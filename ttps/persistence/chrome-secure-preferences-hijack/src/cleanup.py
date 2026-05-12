# flake8: noqa
#!/usr/bin/env python3
"""
Chrome Secure Preferences Exploitation Tool - Cleanup Script

This script reverses the changes made by main.py by restoring files from
backups saved to /tmp/chrome-hijack-backup-<extension_id>/.

Steps:
1. Kill Chrome
2. Restore Secure Preferences from backup
3. Restore manifest.json from backup
4. Restore background script from backup
5. Delete dump.html / dump.js if present
6. Recalculate HMACs and super_mac
7. Remove the backup directory
8. Restart Chrome
"""

import argparse
import hashlib
import hmac
import json
import re
import shutil
import subprocess
import sys
import time
from collections import OrderedDict
from pathlib import Path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Chrome Secure Preferences Exploitation Tool - Cleanup"
    )
    parser.add_argument(
        "--id",
        type=str,
        required=True,
        help="Extension ID that was modified (must match the ID used during exploit)",
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


def get_backup_dir(extension_id):
    """Get the backup directory path for the given extension ID."""
    return Path(f"/tmp/chrome-hijack-backup-{extension_id}")


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
        .replace("\\u2122", "\u2122")
    )
    hash_obj = hmac.new(seed, message.encode("utf-8"), hashlib.sha256)

    return hash_obj.hexdigest().upper()


def calculate_super_mac(json_file, sid, seed):
    """Calculate the super MAC for all preferences."""
    with open(json_file, "r", encoding="utf-8") as json_data:
        data = json.load(json_data, object_pairs_hook=OrderedDict)

    temp = OrderedDict(sorted(data.items()))
    data = temp

    super_msg = sid + json.dumps(data["protection"]["macs"]).replace(" ", "")
    hash_obj = hmac.new(seed, super_msg.encode("utf-8"), hashlib.sha256)
    return hash_obj.hexdigest().upper()


def recalculate_hmacs(secure_prefs_file, sid):
    """Recalculate all HMACs and super_mac for the restored Secure Preferences file.

    After restoring the original Secure Preferences content, we need to recalculate
    the HMACs because the file was written with the original HMAC values which may
    have been invalidated by the restore process.
    """
    seed = b"\xe7H\xf36\xd8^\xa5\xf9\xdc\xdf%\xd8\xf3G\xa6[L\xdffv\x00\xf0-\xf6rJ*\xf1\x8a!-&\xb7\x88\xa2P\x86\x91\x0c\xf3\xa9\x03\x13ihq\xf3\xdc\x05\x8270\xc9\x1d\xf8\xba\\O\xd9\xc8\x84\xb5\x05\xa8"

    try:
        with open(secure_prefs_file, "r", encoding="utf-8") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        # Recalculate HMACs for extensions.settings entries
        if "protection" in data and "macs" in data["protection"]:
            macs = data["protection"]["macs"]
            if "extensions" in macs and "settings" in macs["extensions"]:
                for ext_id, _ in macs["extensions"]["settings"].items():
                    if ext_id in data.get("extensions", {}).get("settings", {}):
                        ext_data = data["extensions"]["settings"][ext_id]
                        path = f"extensions.settings.{ext_id}"
                        ext_dict = json.loads(
                            json.dumps(ext_data), object_pairs_hook=OrderedDict
                        )
                        new_mac = calculate_hmac(ext_dict, path, sid, seed)
                        macs["extensions"]["settings"][ext_id] = new_mac

            # Recalculate developer_mode HMAC if present
            if (
                "extensions" in macs
                and "ui" in macs["extensions"]
                and "developer_mode" in macs["extensions"]["ui"]
            ):
                dev_mode_value = (
                    data.get("extensions", {})
                    .get("ui", {})
                    .get("developer_mode", False)
                )
                path = "extensions.ui.developer_mode"
                new_mac = calculate_hmac(dev_mode_value, path, sid, seed)
                macs["extensions"]["ui"]["developer_mode"] = new_mac

        # Write updated data
        with open(secure_prefs_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

        # Calculate and update the super MAC
        super_mac = calculate_super_mac(secure_prefs_file, sid, seed)
        data["protection"]["super_mac"] = super_mac

        with open(secure_prefs_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

        print("[+] Recalculated HMACs and super_mac")
        return True
    except Exception as e:
        print(f"[!] Error recalculating HMACs: {e}")
        return False


def launch_chrome():
    """Launch Chrome with restore-last-session."""
    print("[*] Launching Chrome...")
    try:
        subprocess.run(
            ["open", "-a", "Google Chrome", "--args", "--restore-last-session"],
            check=True,
        )
        print("[*] Waiting 5 seconds for Chrome to start...")
        time.sleep(5)
        print("[+] Chrome launched successfully")
        return True
    except Exception as e:
        print(f"[!] Error launching Chrome: {e}")
        return False


def restore_profile(profile_backup_dir, device_id):
    """Restore a single Chrome profile from its backup directory."""
    print(f"\n[*] Restoring profile: {profile_backup_dir.name}")

    # Restore Secure Preferences
    secure_prefs_path_file = profile_backup_dir / "secure_prefs_path.txt"
    secure_prefs_backup = profile_backup_dir / "Secure Preferences"
    if secure_prefs_backup.exists() and secure_prefs_path_file.exists():
        original_path = Path(secure_prefs_path_file.read_text().strip())
        shutil.copy2(secure_prefs_backup, original_path)
        print(f"[+] Restored Secure Preferences to {original_path}")

        # Recalculate HMACs for the restored file
        recalculate_hmacs(original_path, device_id)
    else:
        print("[!] Secure Preferences backup not found, skipping restore")

    # Restore manifest.json
    extension_dir_path_file = profile_backup_dir / "extension_dir_path.txt"
    manifest_backup = profile_backup_dir / "manifest.json"
    if manifest_backup.exists() and extension_dir_path_file.exists():
        extension_dir = Path(extension_dir_path_file.read_text().strip())
        shutil.copy2(manifest_backup, extension_dir / "manifest.json")
        print(f"[+] Restored manifest.json to {extension_dir}")
    else:
        print("[!] manifest.json backup not found, skipping restore")

    # Restore background script
    bg_script_backup = profile_backup_dir / "background_script.js"
    bg_script_path_file = profile_backup_dir / "background_script_path.txt"
    if bg_script_backup.exists() and bg_script_path_file.exists():
        original_bg_path = Path(bg_script_path_file.read_text().strip())
        shutil.copy2(bg_script_backup, original_bg_path)
        print(f"[+] Restored background script to {original_bg_path}")
    else:
        print("[!] Background script backup not found, skipping restore")

    # Delete dump.html and dump.js if present
    if extension_dir_path_file.exists():
        extension_dir = Path(extension_dir_path_file.read_text().strip())
        for dump_file in ["dump.html", "dump.js"]:
            dump_path = extension_dir / dump_file
            if dump_path.exists():
                dump_path.unlink()
                print(f"[+] Removed {dump_file}")


def main():
    """Main cleanup function."""
    check_macos()
    args = parse_arguments()
    extension_id = args.id

    backup_dir = get_backup_dir(extension_id)

    if not backup_dir.exists():
        print(f"[!] Backup directory not found: {backup_dir}")
        print("[!] Cannot perform cleanup without backups.")
        return 1

    # Kill Chrome before restoring files
    kill_chrome()

    # Get device ID for HMAC recalculation
    device_id = get_device_id()
    print(f"[*] Device ID: {device_id}")

    # Restore each profile from its backup subdirectory
    profile_count = 0
    for profile_backup_dir in sorted(backup_dir.iterdir()):
        if not profile_backup_dir.is_dir():
            continue
        restore_profile(profile_backup_dir, device_id)
        profile_count += 1

    if profile_count == 0:
        print("[!] No profile backups found in backup directory")
        return 1

    print(f"\n[+] Restored {profile_count} profile(s)")

    # Remove the backup directory
    shutil.rmtree(backup_dir)
    print(f"[+] Removed backup directory: {backup_dir}")

    # Restart Chrome
    launch_chrome()

    print("[+] Cleanup completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
