#include <Windows.h>

BOOL APIENTRY
DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
  if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
    HKEY hKey;
    if (RegCreateKeyExA(
            HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0,
            NULL,
            0,
            KEY_WRITE,
            NULL,
            &hKey,
            NULL) == ERROR_SUCCESS) {
      const char* data = "C:\\Windows\\System32\\calc.exe";
      RegSetValueExA(
          hKey, "Calculator", 0, REG_SZ, (const BYTE*)data, strlen(data) + 1);
      RegCloseKey(hKey);
    }
  }
  return TRUE;
}
