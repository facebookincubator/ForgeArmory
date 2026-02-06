# flake8: noqa


import ctypes
import hashlib
import logging
import os
import ssl
import urllib.error
import urllib.request
from ctypes import create_unicode_buffer, wintypes

# Constants

IOCTL_TERMINATE_PROCESS = 0xB4A00404
SERVICE_KERNEL_DRIVER = 0x00000001
SERVICE_DEMAND_START = 0x00000003
SERVICE_ERROR_IGNORE = 0x00000000
SERVICE_ERROR_NORMAL = 0x00000001
SC_MANAGER_ALL_ACCESS = 0xF003F
SERVICE_ALL_ACCESS = 0xF01FF
SERVICE_CONTROL_STOP = 0x00000001
ERROR_SERVICE_ALREADY_RUNNING = 1056
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
MAX_PATH = 260
_TH32CS_SNAPPROCESS = 0x00000002


class WindowsAPIFunctions:
    def __init__(self):
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        self.psapi = ctypes.WinDLL("Psapi.dll", use_last_error=True)
        self._define_functions()

    def _define_functions(self):
        self.OpenSCManager = self.advapi32.OpenSCManagerW
        self.OpenSCManager.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR, wintypes.DWORD]
        self.OpenSCManager.restype = wintypes.HANDLE

        self.CreateService = self.advapi32.CreateServiceW
        self.CreateService.argtypes = [
            wintypes.HANDLE,
            wintypes.LPWSTR,
            wintypes.LPWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPWSTR,
            wintypes.LPWSTR,
            wintypes.LPDWORD,
            wintypes.LPWSTR,
            wintypes.LPWSTR,
            wintypes.LPWSTR,
        ]
        self.CreateService.restype = wintypes.HANDLE

        self.OpenService = self.advapi32.OpenServiceW
        self.OpenService.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD]
        self.OpenService.restype = wintypes.HANDLE

        self.StartService = self.advapi32.StartServiceW
        self.StartService.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR]
        self.StartService.restype = wintypes.BOOL

        self.ControlService = self.advapi32.ControlService
        self.ControlService.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            ctypes.POINTER(SERVICE_STATUS),
        ]
        self.ControlService.restype = wintypes.BOOL

        self.DeleteService = self.advapi32.DeleteService
        self.DeleteService.argtypes = [wintypes.HANDLE]
        self.DeleteService.restype = wintypes.BOOL

        self.CloseServiceHandle = self.advapi32.CloseServiceHandle
        self.CloseServiceHandle.argtypes = [wintypes.HANDLE]
        self.CloseServiceHandle.restype = wintypes.BOOL

        self.QueryServiceStatus = self.advapi32.QueryServiceStatus
        self.QueryServiceStatus.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(SERVICE_STATUS),
        ]
        self.QueryServiceStatus.restype = wintypes.BOOL

        self.CreateFileW = self.kernel32.CreateFileW
        self.CreateFileW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ]
        self.CreateFileW.restype = wintypes.HANDLE

        self.DeviceIoControl = self.kernel32.DeviceIoControl
        self.DeviceIoControl.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.LPDWORD,
            wintypes.LPVOID,
        ]
        self.DeviceIoControl.restype = wintypes.BOOL

        self.CloseHandle = self.kernel32.CloseHandle
        self.CloseHandle.argtypes = [wintypes.HANDLE]
        self.CloseHandle.restype = wintypes.BOOL

        self.EnumProcesses = self.psapi.EnumProcesses
        self.EnumProcesses.argtypes = [
            ctypes.POINTER(wintypes.DWORD),
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
        ]
        self.EnumProcesses.restype = wintypes.BOOL

        self.GetProcessImageFileNameW = self.psapi.GetProcessImageFileNameW
        self.GetProcessImageFileNameW.argtypes = [
            wintypes.HANDLE,
            wintypes.LPWSTR,
            wintypes.DWORD,
        ]
        self.GetProcessImageFileNameW.restype = wintypes.DWORD

        self.OpenProcess = self.kernel32.OpenProcess
        self.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.OpenProcess.restype = wintypes.HANDLE


# Structures
class SERVICE_STATUS(ctypes.Structure):
    _fields_ = [
        ("dwServiceType", wintypes.DWORD),
        ("dwCurrentState", wintypes.DWORD),
        ("dwControlsAccepted", wintypes.DWORD),
        ("dwWin32ExitCode", wintypes.DWORD),
        ("dwServiceSpecificExitCode", wintypes.DWORD),
        ("dwCheckPoint", wintypes.DWORD),
        ("dwWaitHint", wintypes.DWORD),
    ]


def raise_windows_error():
    error_code = ctypes.get_last_error()
    if error_code != 0:
        raise ctypes.WinError(error_code)


def get_pid_by_name(api, process_name):
    try:
        # Dynamically allocate memory for process IDs
        initial_array_size = 1024
        while True:
            process_ids = (wintypes.DWORD * initial_array_size)()
            cb = ctypes.sizeof(process_ids)
            bytes_returned = wintypes.DWORD()

            if not api.EnumProcesses(process_ids, cb, ctypes.byref(bytes_returned)):
                raise ctypes.WinError(ctypes.get_last_error())

            if bytes_returned.value < cb:
                break
            initial_array_size *= 2

        num_processes = bytes_returned.value // ctypes.sizeof(wintypes.DWORD)

        # Convert process_name to lowercase for case-insensitive comparison
        process_name_lower = process_name.lower()

        for i in range(num_processes):
            process_id = process_ids[i]
            if process_id == 0:
                continue

            h_process = api.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION, False, process_id
            )
            if h_process:
                try:
                    # Use Unicode version of GetProcessImageFileName
                    image_file_name = ctypes.create_unicode_buffer(MAX_PATH)
                    if (
                        api.GetProcessImageFileNameW(
                            h_process, image_file_name, MAX_PATH
                        )
                        > 0
                    ):
                        filename = image_file_name.value.split("\\")[-1].lower()
                        if filename == process_name_lower:
                            logging.info(
                                f"Found process {process_name} with PID {process_id}"
                            )
                            return process_id
                finally:
                    api.CloseHandle(h_process)

    except WindowsError as we:
        logging.error(f"Windows error occurred: {we}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    # logging.warning(f"Process {process_name} not found")
    return None


def download_file(url, local_path, expected_hash=None):
    try:
        if not url.startswith("https://"):
            logging.warning(
                "URL is not using HTTPS. This is not recommended for downloading sensitive files."
            )
            return False

        ssl_context = ssl.create_default_context()

        with (
            urllib.request.urlopen(url, context=ssl_context) as response,
            open(local_path, "wb") as out_file,
        ):
            sha256_hash = hashlib.sha256()
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                out_file.write(chunk)
                sha256_hash.update(chunk)

        if expected_hash:
            calculated_hash = sha256_hash.hexdigest()
            if calculated_hash.lower() != expected_hash.lower():
                logging.error(
                    f"Hash mismatch. Expected: {expected_hash}, Got: {calculated_hash}"
                )
                os.remove(local_path)
                return False
            logging.debug("File hash verified successfully.")

        return True

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        if os.path.exists(local_path):
            os.remove(local_path)
        return False


def load_driver(api, service_name, driver_path, driver_url=None, driver_sha256=None):
    logging.debug(f"Checking driver path: {driver_path}")
    if not os.path.exists(driver_path):
        if driver_url:
            logging.info(
                f"Driver not found at {driver_path}. Attempting to download from {driver_url}"
            )
            if download_file(driver_url, driver_path, driver_sha256):
                logging.info(f"Driver successfully downloaded to {driver_path}")
            else:
                raise FileNotFoundError(f"Failed to download driver from {driver_url}")
        else:
            raise FileNotFoundError(
                f"Driver file {driver_path} does not exist and no download URL provided."
            )

    if not os.path.exists(driver_path):
        raise FileNotFoundError(
            f"Driver file {driver_path} does not exist after download attempt."
        )

    if os.path.getsize(driver_path) == 0:
        raise ValueError(f"Driver file {driver_path} is empty.")

    logging.info("Connecting to Service Control Manager")
    scm = api.OpenSCManager(None, None, SC_MANAGER_ALL_ACCESS)
    if not scm:
        logging.error("Failed to connect to the service control manager")
        raise_windows_error()

    service = None
    try:
        logging.debug(f"Opening service: {service_name}")
        service = api.OpenService(
            scm, create_unicode_buffer(service_name), SERVICE_ALL_ACCESS
        )
        if not service:
            logging.info("Service does not exist. Creating service.")
            service = api.CreateService(
                scm,
                create_unicode_buffer(service_name),
                create_unicode_buffer(service_name),
                SERVICE_ALL_ACCESS,
                SERVICE_KERNEL_DRIVER,
                SERVICE_DEMAND_START,
                SERVICE_ERROR_NORMAL,
                create_unicode_buffer(driver_path),
                None,
                None,
                None,
                None,
                None,
            )
            if not service:
                logging.error(f"Failed to create the service {service_name}")
                raise_windows_error()
            logging.info(f"Service {service_name} created successfully.")
        else:
            logging.info(f"Service {service_name} already exists.")

        if not api.StartService(service, 0, None):
            error_code = ctypes.get_last_error()
            if error_code == ERROR_SERVICE_ALREADY_RUNNING:
                logging.info(f"Service {service_name} is already running.")
            else:
                logging.warning(
                    f"Failed to start the service {service_name}, or the service is already running! Error: {error_code}"
                )
        else:
            logging.info(f"Service {service_name} started successfully.")
    finally:
        if service:
            api.CloseServiceHandle(service)
        api.CloseServiceHandle(scm)


def unload_driver(api, service_name, driver_path, remove_driver=False):
    logging.debug("Connecting to Service Control Manager")
    scm = api.OpenSCManager(None, None, SC_MANAGER_ALL_ACCESS)
    if not scm:
        raise_windows_error()

    service = None
    try:
        logging.debug(f"Opening service: {service_name}")
        service = api.OpenService(
            scm, create_unicode_buffer(service_name), SERVICE_ALL_ACCESS
        )
        if not service:
            raise_windows_error()

        logging.debug(f"Stopping service: {service_name}")
        if not api.ControlService(
            service, SERVICE_CONTROL_STOP, ctypes.byref(SERVICE_STATUS())
        ):
            logging.error(f"Failed to immediately stop the {service_name} service.")
        else:
            logging.info(f"Service {service_name} stopped successfully.")

        if not api.DeleteService(service):
            logging.error(f"Failed to delete the {service_name} service.")
        else:
            logging.info(f"Service {service_name} marked for deletion.")
    finally:
        if service:
            api.CloseServiceHandle(service)
        api.CloseServiceHandle(scm)

    if remove_driver:
        try:
            logging.info(f"Removing driver file: {driver_path}")
            os.chmod(driver_path, 0o777)  # Ensure file is writable
            os.remove(driver_path)
            logging.info(f"Driver file {driver_path} removed.")
        except OSError as e:
            logging.error(f"Error removing driver file: {e}")
