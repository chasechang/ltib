%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define git-branch imx-3.14.28-r0

Summary         : Linux kernel (core of the Linux operating system)
Name            : kernel
Version         : 3.14.28
Release         : 1
License         : GPL
Vendor          : Retronix
Packager        : Chase Chang
Group           : System Environment/Kernel
Source          : ssh://gitolite@10.69.99.252/Kernel/linux-imx-3.10.x.git
URL             : http://www.kernel.org/
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%define buildsubdir kernel-%{version}

%Description
%{summary}

%Prep
%setup -c


%Build

# Allow variables to be expanded
PKG_KERNEL_PATH_PRECONFIG=$(eval echo $PKG_KERNEL_PATH_PRECONFIG)
PKG_KERNEL_KBUILD_PRECONFIG=$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)
PKG_KERNEL_PRECONFIG=$(eval echo $PKG_KERNEL_PRECONFIG)
DTC_NAMES=$(eval echo $SYSCFG_DTC_NAME)

KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-%{_builddir}/%{buildsubdir}}
%{!?showsrcpath: %define showsrcpath 0}
%if %{showsrcpath}
%{echo:%(eval echo ${PKG_KERNEL_PATH_PRECONFIG:-%{_builddir}/%{buildsubdir}})}
%endif

: ${LINTARCH:?must be set to the kernel architecture name}
: ${BUILDCC:?must be set to the token for your build machines compiler}
: ${PKG_KERNEL_PRECONFIG:?must be set to the name of your .config file}
: ${PLATFORM_PATH:?must be set to your ltib platform path}
: ${KSRC_DIR:?cannot find source directory (PKG_KERNEL_PATH_PRECONFIG)}

# I'm not sure if this bit is right.  Do packages need the build
# output, or the source tree?
# I'm not sure if this bit is right.  Do packages need the build
# output, or the source tree?
if [ -L $RPM_BUILD_DIR/linux ]
then
    rm -f $RPM_BUILD_DIR/linux
fi
if [ ! -e $RPM_BUILD_DIR/linux ]
then
    ln -s %{buildsubdir} $RPM_BUILD_DIR/linux
fi

# From now on it won't matter if KBOUT is relative or absolute; 
# if it's relative it must be relative to KSRC_DIR
# cd $KSRC_DIR

KBOUT=$PKG_KERNEL_KBUILD_PRECONFIG
if [ -n "$KBOUT" -a "$KBOUT" != "." ]
then
    # this is to work with symlinked kernel souce trees
    test -d $KBOUT || mkdir -p $KBOUT
    export KBUILD_OUTPUT=$KBOUT
else
    KBOUT="."
fi

KTARG=zImage

SYSCFG_KTARG=${SYSCFG_KTARG:-$KTARG}

#
# This section makes sure there is a .config in the kernel build directory
#
if [ "$PKG_KERNEL_PRECONFIG" = "defconfig" ]
then
    # this is mutated to prevent picking up the BSP defconfig
    PKG_KERNEL_PRECONFIG=kerneldefconfig
fi
for CFG in "$PLATFORM_PATH/${PKG_KERNEL_PRECONFIG}.dev" "$PLATFORM_PATH/$PKG_KERNEL_PRECONFIG" "$KSRC_DIR/rtxconfig/$PKG_KERNEL_PRECONFIG"
do
   if [ -f $CFG ]
   then
       CFG_PATH=$CFG
       break
   fi
done
if [ -z "$CFG_PATH" ]
then
    for DIR in "arch/$GNUTARCH/configs/" "arch/$LINTARCH/configs/"
    do
       if [ -d $DIR ]
       then
           CFG="`find $DIR -name $PKG_KERNEL_PRECONFIG`"
           if [ -n "$CFG" ]
           then
               CFG_PATH=$CFG
               break
           fi
       fi
    done
fi

# PPC_MERGE used to be the primary way of detecting whether
# arch should be powerpc instead of ppc.  Starting in 2.6.28
# this symbol has gone from arch/powerpc/Kconfig and so we
# can't use this as the written back .config file has this
# symbol removed.  Hence the extra checks
if [ $LINTARCH = ppc -a -f arch/powerpc/Kconfig ]
then
    if ! grep -q PPC_MERGE arch/powerpc/Kconfig
    then
        LINTARCH=powerpc
    else
        if [ -n "$CFG_PATH" ]
        then
            if grep -q 'CONFIG_PPC_MERGE=y' $CFG_PATH
            then
                LINTARCH=powerpc
            fi
        else
            LINTARCH=powerpc
        fi
    fi
fi

#
# Check for ltib full rebuilds (e.g. change of toolchain) if so
# force a build from scratch
#
unset PLATFORM

if [ -n "$LTIB_FULL_REBUILD" ]
then
    make ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" mrproper
fi

if [ -n "$CFG_PATH" ]
then
   cp -f $CFG_PATH $KBOUT/.config
else
   echo "Warning: cannot find a config file for the kernel"
fi

#
# configure
#
if [ -z "$LTIB_BATCH" -a -n "$PKG_KERNEL_WANT_CF" -o -n "$SCB_WANT_CF" ]
then
    make ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" menuconfig
else
    if [ -n "$CFG_PATH" ]
    then
        cp -f $CFG_PATH $KBOUT/.config
        yes "" | make ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" oldconfig
    else
        if [ "$PKG_KERNEL_PRECONFIG" = "kerneldefconfig" ]
        then
            PKG_KERNEL_PRECONFIG=defconfig
        fi
        yes "" | make ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" $PKG_KERNEL_PRECONFIG
    fi
fi

# copy back if there was a config file and it changed
if [ -f "$CFG_PATH"  ] && ! diff -q $KBOUT/.config $CFG_PATH
then
    cp -f $KBOUT/.config $PLATFORM_PATH/${PKG_KERNEL_PRECONFIG}.dev
fi

# The first time conf builds, a spurious .config gets made in
# the source directory, this gets rid of it otherwise the kernel
# will not build complaining that the source tree is not clean
if [ -n "$KBUILD_OUTPUT" ]
then
    rm -f .config
fi

#
# Have to specify LOCALVERSION= in the 'make image' command if we
# are setting localversion.  For >= 2.6.35
#
if grep -q 'VERSION = 2' Makefile && \
   grep -q 'PATCHLEVEL = 6' Makefile && \
   grep -q 'CONFIG_LOCALVERSION_AUTO is not' $KBOUT/.config
then
   sublevel="$(grep 'SUBLEVEL =' Makefile | cut -d' ' -f3)"
   if [ "$sublevel" -gt 34 ]; then
     echo "Manually setting LOCALVERSION"
     LOCV='LOCALVERSION='
   fi
fi

#
# Make dep only needs to be done for 2.4 kernels
#
if [ "%{kernel_series}" = "2.4" ]
then
    make ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="${BUILDCC}" dep
fi
#
# build the kernel and optionally the modules
#
# make $LOCV ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" CFLAGS_KERNEL=-mno-unaligned-access $SYSCFG_KTARG
make $LOCV ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" $SYSCFG_KTARG LOADADDR=$SYSCFG_KERNEL_LOADADDR

DTC_NAMES=${DTC_NAMES:-no-dtc}
if [ "$DTC_NAMES" != "no-dtc" ]
then
    make $LOCV ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" $DTC_NAMES
fi

if grep -q '^CONFIG_MODULES=' $KBOUT/.config
then
    # make $LOCV ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" CFLAGS_KERNEL=-mno-unaligned-access modules
    make $LOCV ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" modules
fi

# cscope index
if [ -n "$PKG_KERNEL_WANT_CSCOPE" ]
then
    make ARCH=$LINTARCH cscope
fi

%Install
%define __os_install_post %{nil}

# Allow variables to be expanded
PKG_KERNEL_PATH_PRECONFIG=$(eval echo $PKG_KERNEL_PATH_PRECONFIG)
PKG_KERNEL_KBUILD_PRECONFIG=$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)
DTC_NAMES=$(eval echo $SYSCFG_DTC_NAME)
SYSCFG_DTC_PATH=$(eval echo $SYSCFG_DTC_PATH)

DTC_PAD=${SYSCFG_DTC_PAD:-%dtc_pad}
if [ "$DTC_PAD" = "%%dtc_pad" ]
then
    DTC_PAD=1024
fi

KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-%{_builddir}/%{buildsubdir}}

# From now on it won't matter if KBOUT is relative or absolute; if it's relative it must be relative
# to KSRC_DIR
#cd $KSRC_DIR

KBOUT=$PKG_KERNEL_KBUILD_PRECONFIG
if [ -n "$KBOUT" ]
then
    # this is to work with symlinked kernel souce trees
    test -d $KBOUT || mkdir -p $KBOUT
    export KBUILD_OUTPUT=$KBOUT
else
    KBOUT="."
fi

if [ $LINTARCH = ppc -a -f arch/powerpc/Kconfig ]
then
    if ! grep -q PPC_MERGE arch/powerpc/Kconfig
    then
        LINTARCH=powerpc
    elif grep -q 'CONFIG_PPC_MERGE=y' $KBOUT/.config
    then
        LINTARCH=powerpc
    fi
fi

case $LINTARCH in
    m68k*)
        BOOT_KERNEL=arch/$LINTARCH/boot/uImage
        ;;
    ppc)
        BOOT_KERNEL=arch/$LINTARCH/boot/images/uImage
        ;;
    powerpc)
        BOOT_KERNEL=arch/$LINTARCH/boot/uImage
        ;;
    *)
        if grep -q 'CONFIG_XIP_KERNEL=y' $KBOUT/.config
        then
            BOOT_KERNEL=arch/$LINTARCH/boot/xipImage
        else
            BOOT_KERNEL=arch/$LINTARCH/boot/zImage
        fi
        ;;
esac

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot

if grep -q '^CONFIG_MODULES=' $KBOUT/.config
then
    make ARCH=$LINTARCH HOSTCC="$BUILDCC" DEPMOD=/bin/true INSTALL_MOD_PATH=$RPM_BUILD_ROOT/%{pfx} modules_install
    KERNEL_VER=`ls $RPM_BUILD_ROOT/%{pfx}/lib/modules`
    
    #for i in build source
    #do
    #    rm -f $RPM_BUILD_ROOT/%{pfx}/lib/modules/$KERNEL_VER/$i
    #    ln -s /usr/src/linux $RPM_BUILD_ROOT/%{pfx}/lib/modules/$KERNEL_VER/$i
    #done
fi

SYSCFG_BOOT_KERNEL=${SYSCFG_BOOT_KERNEL:-$BOOT_KERNEL}
if [ -n "$PKG_KERNEL_WANT_OBJCOPY" ]
then
    objcopy -O binary $KBOUT/$SYSCFG_BOOT_KERNEL $KBOUT/${SYSCFG_BOOT_KERNEL}.bin
    SYSCFG_BOOT_KERNEL=${SYSCFG_BOOT_KERNEL}.bin
fi

if [ -n "$PKG_KERNEL_WANT_VMLINUX_STRIPPED" ]
then
    strip $KBOUT/vmlinux -o $KBOUT/vmlinux.stripped
    cp $KBOUT/vmlinux.stripped $RPM_BUILD_ROOT/%{pfx}/boot
fi
for i in vmlinux System.map $SYSCFG_BOOT_KERNEL
do
    cp $KBOUT/$i $RPM_BUILD_ROOT/%{pfx}/boot
done
ln -s `basename $SYSCFG_BOOT_KERNEL` $RPM_BUILD_ROOT/%{pfx}/boot/bootable_kernel
cp $KBOUT/.config $RPM_BUILD_ROOT/%{pfx}/boot/linux.config

# handle the Flat Device Tree build
DTC_NAMES=${DTC_NAMES:-no-dtc}
DTC_PATH=${SYSCFG_DTC_PATH:-arch/$LINTARCH/boot/dts}
if [ -f "$DTC_PATH/$DTC_NAMES" ]
then
    cp $DTC_PATH/$DTC_NAMES $RPM_BUILD_ROOT/%{pfx}/boot/.
fi

if [ -n "$PKG_KERNEL_WANT_HEADERS" ]
then
    KERNEL_HDR_PATH=$RPM_BUILD_ROOT/%{pfx}/usr/src/linux
    install -d ${KERNEL_HDR_PATH}/include
    if ! make ARCH=$LINTARCH CROSS_COMPILE= HOSTCC="$BUILDCC" INSTALL_HDR_PATH=${KERNEL_HDR_PATH} headers_install
    then
        for i in asm-${LINTARCH} asm-generic config linux math-emu media mtd net pcmcia rxrpc scsi sound video
        do
            if [ -d include/$i ]
            then
                cp -a include/$i ${KERNEL_HDR_PATH}/include
            fi
        done

        for i in asm config linux
        do
            if [ -d $KBOUT/include/$i ]
            then
                cp -a $KBOUT/include/$i ${KERNEL_HDR_PATH}/include
            fi
        done
    fi
fi


%Clean
rm -rf $RPM_BUILD_ROOT
if [ -z "$PKG_KERNEL_LEAVESRC" ]
then
    rm -f $RPM_BUILD_DIR/linux
fi

%Files
%defattr(-,root,root)
%{pfx}/*
