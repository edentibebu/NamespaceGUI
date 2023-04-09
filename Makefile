KERNEL_SOURCE=/project/scratch01/compile/edentibebu/linux_source/linux

EXTRA_CFLAGS += -DMODULE=1 -D__KERNEL__=1

kern_mod-objs := $(kern_mod-y)
obj-m := kern_mod.o

PHONY: all

all:
	$(MAKE) -C $(KERNEL_SOURCE) ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- M=$(PWD) modules

clean:
	$(MAKE) -C $(KERNEL_SOURCE) ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- M=$(PWD) clean 