# Copyright (c) Meta Platforms, Inc. and affiliates.
# This source code is licensed under the MIT license in the LICENSE file.

from __future__ import annotations

import argparse
import errno
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import main as chrome_main

EXTENSION_ID: str = "a" * 32


def enabled_entry() -> dict[str, object]:
    return {
        "path": f"{EXTENSION_ID}/1.0_0",
        "state": 1,
        "disable_reasons": [],
    }


class DiscoveryTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "Chrome"
        patcher = mock.patch.object(
            chrome_main, "get_chrome_user_data_dir", return_value=self.root
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def add_profile(
        self,
        name: str,
        entry: dict[str, object] | None,
        installed: bool = True,
    ) -> Path:
        profile = self.root / name
        profile.mkdir(parents=True)
        settings = {} if entry is None else {EXTENSION_ID: entry}
        (profile / "Secure Preferences").write_text(
            json.dumps({"extensions": {"settings": settings}}), encoding="utf-8"
        )
        if entry is not None and installed and isinstance(entry.get("path"), str):
            extension = profile / "Extensions" / str(entry["path"])
            extension.mkdir(parents=True)
            (extension / "manifest.json").write_text(
                json.dumps({"manifest_version": 3, "version": "1.0"}),
                encoding="utf-8",
            )
        return profile

    def assert_failure(self, code: str) -> None:
        with self.assertRaises(chrome_main.ChromePrerequisiteError) as raised:
            chrome_main.find_secure_preferences_files(EXTENSION_ID)
        self.assertEqual(raised.exception.code, code)

    def test_installed_enabled_target_is_returned(self) -> None:
        profile = self.add_profile("Default", enabled_entry())
        self.assertEqual(
            chrome_main.find_secure_preferences_files(EXTENSION_ID),
            [
                (
                    profile / "Secure Preferences",
                    profile / "Extensions" / EXTENSION_ID / "1.0_0",
                )
            ],
        )

    def test_missing_chrome_root_is_not_installed(self) -> None:
        self.assert_failure("EXTENSION_NOT_INSTALLED")

    def test_empty_chrome_root_is_not_installed(self) -> None:
        self.root.mkdir()
        self.assert_failure("EXTENSION_NOT_INSTALLED")

    def test_absent_target_is_not_installed(self) -> None:
        self.add_profile("Default", None)
        self.assert_failure("EXTENSION_NOT_INSTALLED")

    def test_retained_disable_metadata_is_not_installation(self) -> None:
        self.add_profile("Default", {"disable_reasons": [1 << 24]}, installed=False)
        self.assert_failure("EXTENSION_NOT_INSTALLED")

    def test_missing_extension_directory_is_not_installed(self) -> None:
        self.add_profile("Default", enabled_entry(), installed=False)
        self.assert_failure("EXTENSION_NOT_INSTALLED")

    def test_missing_manifest_is_not_installed(self) -> None:
        profile = self.add_profile("Default", enabled_entry())
        (profile / "Extensions" / EXTENSION_ID / "1.0_0" / "manifest.json").unlink()
        self.assert_failure("EXTENSION_NOT_INSTALLED")

    def test_disabled_installed_target_is_reported_separately(self) -> None:
        entry = enabled_entry()
        entry["state"] = 0
        self.add_profile("Default", entry)
        self.assert_failure("EXTENSION_DISABLED")

    def test_nonzero_disable_reasons_are_reported_separately(self) -> None:
        for index, reasons in enumerate(([1 << 24], 1 << 24)):
            entry = enabled_entry()
            entry["disable_reasons"] = reasons
            self.add_profile(f"Profile {index}", entry)
        self.assert_failure("EXTENSION_DISABLED")

    def test_zero_disable_reasons_do_not_disable_target(self) -> None:
        for index, reasons in enumerate(([0], 0, [])):
            entry = enabled_entry()
            entry["disable_reasons"] = reasons
            self.add_profile(f"Profile {index}", entry)
        self.assertEqual(
            len(chrome_main.find_secure_preferences_files(EXTENSION_ID)), 3
        )

    def test_disabled_profile_is_not_selected_with_enabled_profile(self) -> None:
        disabled = enabled_entry()
        disabled["disable_reasons"] = [1]
        self.add_profile("Profile 1", disabled)
        enabled = self.add_profile("Default", enabled_entry())
        self.assertEqual(
            chrome_main.find_secure_preferences_files(EXTENSION_ID),
            [
                (
                    enabled / "Secure Preferences",
                    enabled / "Extensions" / EXTENSION_ID / "1.0_0",
                )
            ],
        )

    def test_chrome_root_eperm_is_not_hidden_by_globbing(self) -> None:
        with mock.patch.object(
            Path,
            "iterdir",
            side_effect=PermissionError(errno.EPERM, "Operation not permitted"),
        ):
            self.assert_failure("FILE_ACCESS_DENIED")

    def test_profile_stat_denial_is_not_an_absent_profile(self) -> None:
        self.add_profile("Default", enabled_entry())
        with mock.patch.object(
            Path, "stat", side_effect=PermissionError(errno.EACCES, "denied")
        ):
            self.assert_failure("FILE_ACCESS_DENIED")

    def test_preferences_read_denial_is_not_an_absent_target(self) -> None:
        self.add_profile("Default", enabled_entry())
        with mock.patch("builtins.open", side_effect=PermissionError("denied")):
            self.assert_failure("FILE_ACCESS_DENIED")

    def test_root_io_error_fails_closed(self) -> None:
        with mock.patch.object(
            Path, "iterdir", side_effect=OSError(errno.EIO, "I/O error")
        ):
            self.assert_failure("PROFILE_DATA_UNREADABLE")

    def test_invalid_preferences_json_fails_closed(self) -> None:
        profile = self.add_profile("Default", enabled_entry())
        (profile / "Secure Preferences").write_text("{", encoding="utf-8")
        self.assert_failure("PROFILE_DATA_UNREADABLE")

    def test_invalid_preferences_structure_fails_closed(self) -> None:
        profile = self.add_profile("Default", enabled_entry())
        (profile / "Secure Preferences").write_text("[]", encoding="utf-8")
        self.assert_failure("INVALID_PROFILE_DATA")

    def test_invalid_settings_structure_fails_closed(self) -> None:
        profile = self.add_profile("Default", enabled_entry())
        (profile / "Secure Preferences").write_text(
            json.dumps({"extensions": {"settings": []}}), encoding="utf-8"
        )
        self.assert_failure("INVALID_PROFILE_DATA")

    def test_invalid_disable_reason_structure_fails_closed(self) -> None:
        entry = enabled_entry()
        entry["disable_reasons"] = "not-a-disable-reason"
        self.add_profile("Default", entry)
        self.assert_failure("INVALID_PROFILE_DATA")

    def test_null_disable_reason_fails_closed(self) -> None:
        entry = enabled_entry()
        entry["disable_reasons"] = [None]
        self.add_profile("Default", entry)
        self.assert_failure("INVALID_PROFILE_DATA")

    def test_boolean_disable_reason_fails_closed(self) -> None:
        entry = enabled_entry()
        entry["disable_reasons"] = [False]
        self.add_profile("Default", entry)
        self.assert_failure("INVALID_PROFILE_DATA")

    def test_invalid_enabled_state_fails_closed(self) -> None:
        entry = enabled_entry()
        entry["state"] = "enabled"
        self.add_profile("Default", entry)
        self.assert_failure("INVALID_PROFILE_DATA")

    def test_non_string_path_fails_closed(self) -> None:
        self.add_profile("Default", {"path": 1}, installed=False)
        self.assert_failure("INVALID_PROFILE_DATA")

    def test_invalid_manifest_json_fails_before_modification(self) -> None:
        profile = self.add_profile("Default", enabled_entry())
        (profile / "Extensions" / EXTENSION_ID / "1.0_0" / "manifest.json").write_text(
            "{", encoding="utf-8"
        )
        self.assert_failure("PROFILE_DATA_UNREADABLE")


class LifecycleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.args = argparse.Namespace(
            id=EXTENSION_ID,
            exfil_method="local",
            telegram_token=None,
            telegram_chat_id=None,
            wait_time=15,
            kill_after=False,
        )
        self.operations = mock.Mock()
        for name, result in (
            ("check_macos", True),
            ("parse_arguments", self.args),
            (
                "find_secure_preferences_files",
                [(Path("preferences"), Path("extension"))],
            ),
            ("get_device_id", "test-hardware-uuid"),
            ("chrome_is_running", True),
            ("kill_chrome", None),
            ("modify_chrome_files", True),
            ("launch_chrome", True),
            ("restore_chrome_after_prerequisite_failure", None),
        ):
            patcher = mock.patch.object(chrome_main, name, return_value=result)
            patched = patcher.start()
            self.addCleanup(patcher.stop)
            self.operations.attach_mock(patched, name)
        printer = mock.patch("builtins.print")
        self.printed = printer.start()
        self.addCleanup(printer.stop)

    def assert_no_browser_changes(self) -> None:
        self.operations.kill_chrome.assert_not_called()
        self.operations.modify_chrome_files.assert_not_called()
        self.operations.launch_chrome.assert_not_called()
        self.operations.restore_chrome_after_prerequisite_failure.assert_not_called()

    def test_success_checks_prerequisites_before_stopping(self) -> None:
        self.assertEqual(chrome_main.main(), 0)
        self.assertEqual(
            self.operations.mock_calls,
            [
                mock.call.check_macos(),
                mock.call.parse_arguments(),
                mock.call.find_secure_preferences_files(EXTENSION_ID),
                mock.call.get_device_id(),
                mock.call.chrome_is_running(),
                mock.call.kill_chrome(),
                mock.call.find_secure_preferences_files(EXTENSION_ID),
                mock.call.modify_chrome_files(
                    EXTENSION_ID,
                    "test-hardware-uuid",
                    self.args,
                    found_files=[(Path("preferences"), Path("extension"))],
                ),
                mock.call.launch_chrome(EXTENSION_ID, 15, False),
            ],
        )

    def test_missing_target_leaves_browser_unchanged(self) -> None:
        self.operations.find_secure_preferences_files.side_effect = (
            chrome_main.ChromePrerequisiteError("EXTENSION_NOT_INSTALLED", "missing")
        )
        self.assertEqual(chrome_main.main(), 1)
        self.assert_no_browser_changes()

    def test_denied_profile_leaves_browser_unchanged(self) -> None:
        self.operations.find_secure_preferences_files.side_effect = (
            chrome_main.ChromePrerequisiteError("FILE_ACCESS_DENIED", "denied")
        )
        self.assertEqual(chrome_main.main(), 1)
        self.assert_no_browser_changes()

    def test_disabled_target_leaves_browser_unchanged(self) -> None:
        self.operations.find_secure_preferences_files.side_effect = (
            chrome_main.ChromePrerequisiteError("EXTENSION_DISABLED", "disabled")
        )
        self.assertEqual(chrome_main.main(), 1)
        self.assert_no_browser_changes()

    def test_identity_failure_leaves_browser_unchanged(self) -> None:
        self.operations.get_device_id.side_effect = chrome_main.ChromePrerequisiteError(
            "DEVICE_ID_UNAVAILABLE", "missing"
        )
        self.assertEqual(chrome_main.main(), 1)
        self.assert_no_browser_changes()

    def test_unknown_browser_state_leaves_browser_unchanged(self) -> None:
        self.operations.chrome_is_running.side_effect = (
            chrome_main.ChromePrerequisiteError("BROWSER_STATE_UNAVAILABLE", "unknown")
        )
        self.assertEqual(chrome_main.main(), 1)
        self.assert_no_browser_changes()

    def test_preflight_interrupt_leaves_browser_unchanged(self) -> None:
        self.operations.find_secure_preferences_files.side_effect = KeyboardInterrupt()
        self.assertEqual(chrome_main.main(), 1)
        self.assert_no_browser_changes()

    def test_stop_failure_restores_only_unchanged_session(self) -> None:
        self.operations.kill_chrome.side_effect = chrome_main.ChromePrerequisiteError(
            "BROWSER_STOP_FAILED", "failed"
        )
        self.assertEqual(chrome_main.main(), 1)
        self.operations.modify_chrome_files.assert_not_called()
        self.operations.restore_chrome_after_prerequisite_failure.assert_called_once_with()
        self.operations.launch_chrome.assert_not_called()

    def test_stop_interrupt_restores_unchanged_session(self) -> None:
        self.operations.kill_chrome.side_effect = KeyboardInterrupt()
        self.assertEqual(chrome_main.main(), 1)
        self.operations.modify_chrome_files.assert_not_called()
        self.operations.restore_chrome_after_prerequisite_failure.assert_called_once_with()

    def test_post_stop_discovery_denial_restores_unchanged_session(self) -> None:
        self.operations.find_secure_preferences_files.side_effect = [
            [(Path("preferences"), Path("extension"))],
            chrome_main.ChromePrerequisiteError(
                "FILE_ACCESS_DENIED", "profile changed before writes"
            ),
        ]
        self.assertEqual(chrome_main.main(), 1)
        self.operations.modify_chrome_files.assert_not_called()
        self.operations.restore_chrome_after_prerequisite_failure.assert_called_once_with()
        self.operations.launch_chrome.assert_not_called()

    def test_post_stop_discovery_interrupt_restores_unchanged_session(self) -> None:
        self.operations.find_secure_preferences_files.side_effect = [
            [(Path("preferences"), Path("extension"))],
            KeyboardInterrupt(),
        ]
        self.assertEqual(chrome_main.main(), 1)
        self.operations.modify_chrome_files.assert_not_called()
        self.operations.restore_chrome_after_prerequisite_failure.assert_called_once_with()
        self.operations.launch_chrome.assert_not_called()

    def test_closed_browser_is_not_started_after_discovery_failure(self) -> None:
        self.operations.chrome_is_running.return_value = False
        self.operations.find_secure_preferences_files.side_effect = [
            [(Path("preferences"), Path("extension"))],
            chrome_main.ChromePrerequisiteError("FILE_ACCESS_DENIED", "denied"),
        ]
        self.assertEqual(chrome_main.main(), 1)
        self.operations.modify_chrome_files.assert_not_called()
        self.operations.restore_chrome_after_prerequisite_failure.assert_not_called()
        self.operations.launch_chrome.assert_not_called()

    def test_failed_modification_does_not_restart_changed_extension(self) -> None:
        self.operations.modify_chrome_files.return_value = False
        self.assertEqual(chrome_main.main(), 1)
        self.operations.restore_chrome_after_prerequisite_failure.assert_not_called()
        self.operations.launch_chrome.assert_not_called()
        self.assertTrue(
            any(
                "MODIFICATION_FAILED" in str(call)
                for call in self.printed.call_args_list
            )
        )

    def test_interrupted_modification_does_not_restart_changed_extension(self) -> None:
        self.operations.modify_chrome_files.side_effect = KeyboardInterrupt()
        self.assertEqual(chrome_main.main(), 1)
        self.operations.restore_chrome_after_prerequisite_failure.assert_not_called()
        self.operations.launch_chrome.assert_not_called()

    def test_modification_io_error_does_not_restart_changed_extension(self) -> None:
        self.operations.modify_chrome_files.side_effect = OSError("failed")
        self.assertEqual(chrome_main.main(), 1)
        self.operations.restore_chrome_after_prerequisite_failure.assert_not_called()
        self.operations.launch_chrome.assert_not_called()

    def test_typed_modification_failure_does_not_reopen_changed_files(self) -> None:
        self.operations.modify_chrome_files.side_effect = (
            chrome_main.ChromePrerequisiteError("FILE_ACCESS_DENIED", "during mutation")
        )
        self.assertEqual(chrome_main.main(), 1)
        self.operations.restore_chrome_after_prerequisite_failure.assert_not_called()
        self.operations.launch_chrome.assert_not_called()

    def test_startup_failure_is_not_reported_as_success(self) -> None:
        self.operations.launch_chrome.return_value = False
        self.assertEqual(chrome_main.main(), 1)
        self.assertTrue(
            any(
                "BROWSER_START_FAILED" in str(call)
                for call in self.printed.call_args_list
            )
        )
        self.operations.restore_chrome_after_prerequisite_failure.assert_not_called()

    def test_invalid_remote_arguments_do_not_read_or_stop_browser(self) -> None:
        self.args.exfil_method = "telegram"
        self.assertEqual(chrome_main.main(), 1)
        self.operations.find_secure_preferences_files.assert_not_called()
        self.operations.get_device_id.assert_not_called()
        self.assert_no_browser_changes()


class ProcessHandlingTest(unittest.TestCase):
    def test_missing_hardware_uuid_is_a_prerequisite_failure(self) -> None:
        with mock.patch.object(subprocess, "check_output", return_value="No UUID"):
            with self.assertRaises(chrome_main.ChromePrerequisiteError) as raised:
                chrome_main.get_device_id()
        self.assertEqual(raised.exception.code, "DEVICE_ID_UNAVAILABLE")

    def test_process_lookup_distinguishes_closed_and_unknown(self) -> None:
        with mock.patch.object(subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 1, stderr="")
            self.assertFalse(chrome_main.chrome_is_running())
            run.return_value = subprocess.CompletedProcess(
                [], 2, stderr="lookup failed"
            )
            with self.assertRaises(chrome_main.ChromePrerequisiteError) as raised:
                chrome_main.chrome_is_running()
        self.assertEqual(raised.exception.code, "BROWSER_STATE_UNAVAILABLE")

    def test_nonzero_stop_error_is_not_ignored(self) -> None:
        with mock.patch.object(subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 2)
            with self.assertRaises(chrome_main.ChromePrerequisiteError) as raised:
                chrome_main.kill_chrome()
        self.assertEqual(raised.exception.code, "BROWSER_STOP_FAILED")

    def test_chrome_still_running_is_a_stop_failure(self) -> None:
        with (
            mock.patch.object(subprocess, "run") as run,
            mock.patch.object(chrome_main.time, "sleep"),
            mock.patch.object(chrome_main, "chrome_is_running", return_value=True),
        ):
            run.return_value = subprocess.CompletedProcess([], 0)
            with self.assertRaises(chrome_main.ChromePrerequisiteError) as raised:
                chrome_main.kill_chrome()
        self.assertEqual(raised.exception.code, "BROWSER_STOP_FAILED")

    def test_abort_restore_has_no_post_launch_kill(self) -> None:
        with (
            mock.patch.object(subprocess, "run") as run,
            mock.patch.object(chrome_main, "chrome_is_running", return_value=False),
        ):
            chrome_main.restore_chrome_after_prerequisite_failure()
        run.assert_called_once_with(
            ["open", "-a", "Google Chrome", "--args", "--restore-last-session"],
            check=True,
            timeout=15,
        )

    def test_running_session_is_not_reopened(self) -> None:
        with (
            mock.patch.object(subprocess, "run") as run,
            mock.patch.object(chrome_main, "chrome_is_running", return_value=True),
        ):
            chrome_main.restore_chrome_after_prerequisite_failure()
        run.assert_not_called()

    def test_unknown_session_state_is_not_reopened(self) -> None:
        with (
            mock.patch.object(subprocess, "run") as run,
            mock.patch.object(
                chrome_main,
                "chrome_is_running",
                side_effect=chrome_main.ChromePrerequisiteError(
                    "BROWSER_STATE_UNAVAILABLE", "unknown"
                ),
            ),
        ):
            chrome_main.restore_chrome_after_prerequisite_failure()
        run.assert_not_called()

    def test_restore_failure_keeps_explicit_failure_diagnostic(self) -> None:
        with (
            mock.patch.object(subprocess, "run", side_effect=OSError("restore failed")),
            mock.patch.object(chrome_main, "chrome_is_running", return_value=False),
            mock.patch("builtins.print") as printed,
        ):
            chrome_main.restore_chrome_after_prerequisite_failure()
        self.assertTrue(
            any(
                "BROWSER_RESTORE_FAILED" in str(call) for call in printed.call_args_list
            )
        )

    def test_stop_is_scoped_to_current_user(self) -> None:
        with (
            mock.patch.object(subprocess, "run") as run,
            mock.patch.object(chrome_main.time, "sleep"),
            mock.patch.object(chrome_main, "chrome_is_running", return_value=False),
        ):
            run.return_value = subprocess.CompletedProcess([], 0)
            chrome_main.kill_chrome()
        self.assertEqual(
            run.call_args.args[0],
            ["pkill", "-u", str(chrome_main.os.getuid()), "-a", "-i", "Google Chrome"],
        )


class ModificationResultTest(unittest.TestCase):
    def test_preflight_targets_do_not_trigger_another_discovery(self) -> None:
        targets = [(Path("preferences"), Path("Extensions/one"))]
        with (
            mock.patch.object(chrome_main, "find_secure_preferences_files") as find,
            mock.patch.object(
                chrome_main, "create_background_script", return_value=True
            ),
            mock.patch.object(
                chrome_main, "modify_secure_preferences", return_value=True
            ),
        ):
            self.assertTrue(
                chrome_main.modify_chrome_files(
                    EXTENSION_ID,
                    "test-hardware-uuid",
                    argparse.Namespace(),
                    found_files=targets,
                )
            )
        find.assert_not_called()

    def test_partial_background_failure_is_not_success(self) -> None:
        profiles = [
            (Path("preferences-one"), Path("Extensions/one")),
            (Path("preferences-two"), Path("Extensions/two")),
        ]
        with (
            mock.patch.object(
                chrome_main, "find_secure_preferences_files", return_value=profiles
            ),
            mock.patch.object(
                chrome_main, "create_background_script", side_effect=[True, False]
            ),
            mock.patch.object(
                chrome_main, "modify_secure_preferences", return_value=True
            ) as modify,
        ):
            self.assertFalse(
                chrome_main.modify_chrome_files(
                    EXTENSION_ID, "test-hardware-uuid", argparse.Namespace()
                )
            )
        self.assertEqual(modify.call_count, 1)

    def test_partial_preferences_failure_is_not_success(self) -> None:
        profiles = [
            (Path("preferences-one"), Path("Extensions/one")),
            (Path("preferences-two"), Path("Extensions/two")),
        ]
        with (
            mock.patch.object(
                chrome_main, "find_secure_preferences_files", return_value=profiles
            ),
            mock.patch.object(
                chrome_main, "create_background_script", return_value=True
            ),
            mock.patch.object(
                chrome_main, "modify_secure_preferences", side_effect=[True, False]
            ) as modify,
        ):
            self.assertFalse(
                chrome_main.modify_chrome_files(
                    EXTENSION_ID, "test-hardware-uuid", argparse.Namespace()
                )
            )
        self.assertEqual(modify.call_count, 2)
