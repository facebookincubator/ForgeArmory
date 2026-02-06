# flake8: noqa

import argparse
import ctypes
import logging
import os
import sys
from ctypes import wintypes
from datetime import datetime, timedelta

import win32com.client


def get_user_home_path():
    return os.path.expanduser("~")


def get_current_user():
    # Constants
    MAX_COMPUTERNAME_LENGTH = 31
    COMPUTER_NAME_FORMAT_DNS_DOMAIN = 2
    COMPUTER_NAME_FORMAT_NETBIOS = 0

    # Function prototypes
    GetUserNameW = ctypes.windll.advapi32.GetUserNameW
    GetUserNameW.argtypes = [wintypes.LPWSTR, wintypes.LPDWORD]
    GetUserNameW.restype = wintypes.BOOL

    GetComputerNameExW = ctypes.windll.kernel32.GetComputerNameExW
    GetComputerNameExW.argtypes = [wintypes.DWORD, wintypes.LPWSTR, wintypes.LPDWORD]
    GetComputerNameExW.restype = wintypes.BOOL

    # Get username
    username = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    size = wintypes.DWORD(len(username))
    if not GetUserNameW(username, ctypes.byref(size)):
        return None

    # Try to get DNS domain name
    domain = ctypes.create_unicode_buffer(MAX_COMPUTERNAME_LENGTH + 1)
    size = wintypes.DWORD(len(domain))
    GetComputerNameExW(COMPUTER_NAME_FORMAT_DNS_DOMAIN, domain, ctypes.byref(size))

    # If DNS domain is empty, get NetBIOS name (computer name)
    if not domain.value:
        size = wintypes.DWORD(len(domain))
        if not GetComputerNameExW(
            COMPUTER_NAME_FORMAT_NETBIOS, domain, ctypes.byref(size)
        ):
            return username.value

    return f"{domain.value}\\{username.value}"


# fmt:off
def create_scheduled_task(
    task_name, action_path, action_args, time_trigger, repetition, principal, output_file
):

    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")

        task_def = scheduler.NewTask(0)
        task_def.RegistrationInfo.Description = task_name
        task_def.Settings.Enabled = True
        task_def.Settings.Hidden = False
        task_def.Settings.Priority = 7
        task_def.Settings.AllowDemandStart = True

        action = task_def.Actions.Create(0)
        action.Path = action_path
        action.Arguments = action_args

        trigger = task_def.Triggers.Create(1)
        trigger.StartBoundary = (
            datetime.now() + timedelta(minutes=time_trigger)
        ).isoformat()
        trigger.Enabled = True

        repetition_obj = trigger.Repetition
        repetition_obj.Interval = f"PT{repetition}M"
        repetition_obj.StopAtDurationEnd = False

        task_def.Principal.UserId = principal
        if principal.upper() == "SYSTEM":
            task_def.Principal.LogonType = 5  # TASK_LOGON_SERVICE_ACCOUNT
            task_def.Principal.RunLevel = 1  # TASK_RUNLEVEL_HIGHEST
        else:
            task_def.Principal.LogonType = 3  # TASK_LOGON_INTERACTIVE_TOKEN
            task_def.Principal.RunLevel = 1  # TASK_RUNLEVEL_HIGHEST

        root_folder.RegisterTaskDefinition(
            task_name,
            task_def,
            6,  # TASK_CREATE_OR_UPDATE
            None,
            None,
            5 if principal.upper() == "SYSTEM" else 3,
        )

        print(
            f"Task '{task_name}' has been created and will start in {time_trigger} minute(s)."
        )

    except win32com.client.pywintypes.com_error as e:
        print(f"COM Error: {e.strerror}")
        if e.winerror == -2147024891:  # 0x80070005 ACCESS_DENIED
            print("Access denied. Make sure you have the necessary permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
# fmt:on


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def validate_path(path):
    return os.path.exists(path)


def main():
    parser = argparse.ArgumentParser(description="Create a scheduled task in Windows.")
    parser.add_argument(
        "--name", default="HighPriorityPyCOMTask", help="Name of the task"
    )
    parser.add_argument(
        "--action",
        default=r"C:\Windows\System32\cmd.exe",
        help="Path of the action to execute",
    )
    parser.add_argument(
        "--action-args",
        default=None,
        help="Arguments passed to the action executable (default: '/c whoami > {output_file}')",
    )
    parser.add_argument(
        "--output-file",
        default="current_context.txt",
        help="Output file name for the task",
    )
    parser.add_argument(
        "--trigger", type=int, default=1, help="Minutes until the task starts"
    )
    parser.add_argument(
        "--repeat", type=int, default=30, help="Repeat interval in minutes"
    )
    parser.add_argument(
        "--principal",
        default="SYSTEM",
        help="Principal under which to run the task (SYSTEM or ADMIN)",
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

    if not is_admin():
        print("This script must be run with administrator privileges.")
        sys.exit(1)

    if args.principal.upper() not in ["SYSTEM", "ADMIN"]:
        print("Principal must be either SYSTEM or ADMIN.")
        sys.exit(1)

    if not validate_path(args.action):
        print(f"The specified action path does not exist: {args.action}")
        sys.exit(1)

    if args.repeat < 1:
        print("Repeat interval must be at least 1 minute.")
        sys.exit(1)

    # Get the user's home path
    user_home = get_user_home_path()
    output_file = os.path.join(user_home, args.output_file)

    # Build action args, defaulting to whoami redirect if not specified
    action_args = args.action_args
    if action_args is None:
        action_args = f"/c whoami > {output_file}"

    principal = (
        args.principal if args.principal.upper() == "SYSTEM" else get_current_user()
    )
    print(f"We will be creating the task under the principal {principal}")

    create_scheduled_task(
        args.name,
        args.action,
        action_args,
        args.trigger,
        args.repeat,
        principal,
        output_file,
    )


if __name__ == "__main__":
    main()
