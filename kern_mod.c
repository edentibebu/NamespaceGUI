
/*credentials: https://docs.kernel.org/security/credentials.html*/
/*prepare creds: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/kernel/cred.c?h=v4.19#n230*/
/*commit creds: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/kernel/cred.c?h=v4.19#n409*/
#include <linux/init.h>
#include <linux/module.h>
#include <linux/sched.h>
#include<linux/cred.h>

struct task_struct *task;
struct cred *new_cred;

static int function(){

    /* sets new UID/GID to root permissions.*/
    kuid_t kuid = KUIDT_INIT(0);
    kgid_t kgid = KGIDT_INIT(0);
    //kernel_cap_t kcap_permitted = cap_set();

    /* gets context of current task */
    task = get_current();
    if (task == NULL) {
    printk("Error: Failed to get current task info.\n");
    return -1;
    }

    /* changes privileges */
    new_cred = prepare_creds();
    if (new_cred == NULL) {
    printk("Error: Failed to prepare new credentials\n");
    return -ENOMEM;
    }

    new_cred->uid = kuid;
    new_cred->gid = kgid;
    new_cred->euid = kuid;
    new_cred->egid = kgid;

    new_cred->cap_permitted = kcap_permitted;

    commit_creds(new_cred);
    return 0;
}

//to-do: use cap_permitted to change capabilities


static int kern_mod_init(void)
{
    printk(KERN_INFO "Loaded kern_mod module\n");
    function();
    return 0;
}

static void 
kern_mod_exit(void)
{
    printk(KERN_INFO "Unloaded kern_mod module\n");
}


module_init(kern_mod_init);
module_exit(kern_mod_exit);

MODULE_LICENSE ("GPL");