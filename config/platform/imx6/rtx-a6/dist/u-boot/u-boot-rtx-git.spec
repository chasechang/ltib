%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define git-branch RTX_V2015.04

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 2015.04
Release         : 1
License         : GPL
Vendor          : Retronix
Packager        : Chase Chang
Group           : Applications/System
Source          : ssh://gitolite@10.69.99.252/U-Boot/u-boot-imx.git
URL             : http://www.denx.de/wiki/U-Boot/
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -c

%Build

PKG_U_BOOT_CONFIG_TYPE=${PKG_U_BOOT_CONFIG_TYPE:-rtx_q7_mx6q_defconfig}
make HOSTCC="$BUILDCC" CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_CONFIG_TYPE
make HOSTCC="$BUILDCC" HOSTSTRIP="$BUILDSTRIP" \
     CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_BUILD_ARGS all

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
for i in u-boot.imx u-boot.bin u-boot
do
    cp $i $RPM_BUILD_ROOT/%{pfx}/boot
done

%Clean
rm -rf $RPM_BUILD_ROOT
if [ -z "$PKG_U_BOOT_LEAVESRC" ]
then
    rm -rf $RPM_BUILD_DIR/%{name}-%{version}
fi

%Files
%defattr(-,root,root)
%{pfx}/*
