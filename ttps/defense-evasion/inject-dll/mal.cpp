#include <Windows.h>

DWORD WINAPI OpenNotepadThread(LPVOID) {
  STARTUPINFOA si = {sizeof(si)};
  PROCESS_INFORMATION pi = {0};
  char cmd[] = "notepad.exe";
  if (CreateProcessA(NULL, cmd, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
  }
  return 0;
}

BOOL APIENTRY
DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
  if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
    HANDLE hThread = CreateThread(NULL, 0, OpenNotepadThread, NULL, 0, NULL);
    if (hThread)
      CloseHandle(hThread);
  }
  return TRUE;
}
