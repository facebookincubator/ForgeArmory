#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

MODULE_LICENSE("MIT");
MODULE_AUTHOR("tbarabosch");
MODULE_DESCRIPTION("Basic LKM to load as rootkit simulation");
MODULE_VERSION("1.0");

static int __init lkm_init(void) {
  printk(KERN_INFO "LKM has loaded\n");
  return 0;
}

module_init(lkm_init);
