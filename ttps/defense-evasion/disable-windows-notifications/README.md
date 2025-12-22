# Disable Windows Notifications

## Description
Disables Windows notification systems (Defender notifications, Security Center, toast notifications, notification center, Defender UX) to suppress security alerts. Employed by Redline Stealer, Azorult, and Remcos RAT to operate silently without alerting users.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-windows-notifications/ttp.yaml
```

## Steps
1. **disable_defender_notification**: Sets DisableNotifications to 1 in the Windows Defender Security Center\Notifications registry key, disabling all Windows Defender notifications.
2. **suppress_defender_notifications**: Sets Notification_Suppress to 1 in the Windows Defender\UX Configuration registry key, suppressing Windows Defender user interface notifications.
3. **disable_security_center_notifications**: Sets UseActionCenterExperience to 0 in the ImmersiveShell registry key, disabling Windows Security Center notifications.
4. **disable_toast_notifications**: Sets ToastEnabled to 0 in the PushNotifications registry key, disabling all toast (pop-up) notifications.
5. **disable_notification_center**: Sets DisableNotificationCenter to 1 in the Windows\Explorer Policies registry key, disabling the Windows notification center (action center).
