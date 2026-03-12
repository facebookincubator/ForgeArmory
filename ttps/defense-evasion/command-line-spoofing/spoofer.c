#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <sys/prctl.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
  const char* new_name = argv[1];

  prctl(PR_SET_NAME, (unsigned long)new_name, 0, 0, 0);

  strncpy(argv[0], new_name, strlen(argv[0]));

  printf("Process name spoofed to: %s\n", new_name);
  // Keep process alive to check the process name manually
  sleep(10);
  return 0;
}
