// @nolint
#include <direct.h>
#include <shlobj.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#pragma comment(lib, "shell32.lib")

#define PATH_SEPARATOR ";"
#define PYTHON_EXE "python.exe"
#define PYTHON3_EXE "python3.exe"
#define SCRIPT_NAME "script.py"

const char* PYTHON_SCRIPT =
    "import os\n"
    "import getpass\n"
    "import sys\n"
    "\n"
    "def gather_info():\n"
    "    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))\n"
    "    current_dir = os.getcwd()\n"
    "    files = os.listdir(current_dir)\n"
    "    env_vars = dict(os.environ)\n"
    "    user = getpass.getuser()\n"
    "\n"
    "    output_file = os.path.join(script_dir, 'gathered.txt')\n"
    "    with open(output_file, 'w') as f:\n"
    "        f.write(f'Script Directory: {script_dir}\\n')\n"
    "        f.write(f'Current Working Directory: {current_dir}\\n')\n"
    "        f.write(f'Files in Current Directory: {files}\\n')\n"
    "        f.write(f'Environment Variables: {env_vars}\\n')\n"
    "        f.write(f'Logged in User: {user}\\n')\n"
    "\n"
    "    print(f'Information gathered and saved to {output_file}')\n"
    "\n"
    "if __name__ == '__main__':\n"
    "    gather_info()\n";

char* find_python_in_path() {
  const char* path = getenv("PATH");
  if (path == NULL)
    return NULL;

  char* path_copy = _strdup(path);
  if (path_copy == NULL)
    return NULL;

  char* dir = strtok(path_copy, PATH_SEPARATOR);
  while (dir != NULL) {
    char full_path[MAX_PATH];
    DWORD attrib;

    const char* exes[] = {PYTHON_EXE, PYTHON3_EXE};
    for (int i = 0; i < 2; i++) {
      if (dir[strlen(dir) - 1] == '\\') {
        snprintf(full_path, sizeof(full_path), "%s%s", dir, exes[i]);
      } else {
        snprintf(full_path, sizeof(full_path), "%s\\%s", dir, exes[i]);
      }

      attrib = GetFileAttributesA(full_path);
      if (attrib != INVALID_FILE_ATTRIBUTES &&
          !(attrib & FILE_ATTRIBUTE_DIRECTORY)) {
        char* result = _strdup(full_path);
        free(path_copy);
        return result;
      }
    }

    dir = strtok(NULL, PATH_SEPARATOR);
  }

  free(path_copy);
  return NULL;
}

int main() {
  char* python_path = find_python_in_path();
  if (python_path == NULL) {
    printf("Python not found in PATH\n");
    return 1;
  }
  printf("Python found at: %s\n", python_path);

  char home_path[MAX_PATH];
  if (SUCCEEDED(SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, 0, home_path))) {
    printf("Home directory: %s\n", home_path);

    char script_path[MAX_PATH];
    snprintf(
        script_path, sizeof(script_path), "%s\\%s", home_path, SCRIPT_NAME);

    // Write the Python script to a file
    FILE* script_file = fopen(script_path, "w");
    if (script_file == NULL) {
      printf("Failed to create Python script\n");
      printf("Error: %s\n", strerror(errno));
      free(python_path);
      return 1;
    }
    fprintf(script_file, "%s", PYTHON_SCRIPT);
    fclose(script_file);

    printf("Script created at: %s\n", script_path);

    // Check if the script file exists
    if (GetFileAttributesA(script_path) == INVALID_FILE_ATTRIBUTES) {
      printf("Error: Script file does not exist or is not accessible.\n");
      free(python_path);
      return 1;
    }

    // Execute the Python script
    char command[MAX_PATH * 2];
    snprintf(
        command,
        sizeof(command),
        "\"\"%s\" \"%s\"\"",
        python_path,
        script_path);

    // Debug: Print the command before execution
    printf("Executing command: %s\n", command);

    int result = system(command);
    if (result == 0) {
      printf("Python script executed successfully\n");
    } else {
      printf("Python script execution failed with status: %d\n", result);
      printf("Error: %s\n", strerror(errno));
    }
  } else {
    printf("Failed to get user's home directory\n");
    printf("Error: %s\n", strerror(errno));
  }

  free(python_path);
  return 0;
}
