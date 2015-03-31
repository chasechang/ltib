%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Raspberry Pi /boot partition
Name            : rpi_boot
Version         : 5dd9b49
Release         : 1
License         : GPL2, Broadcom
Vendor          : Raspberry Pi Foundation
URL             : https://github.com/raspberrypi/firmware/tree/master/boot
Group           : Boot
Packager        : Sean Malloy
Source0         : %{name}-%{version}.tar.gz
Source1         : rpi_boot_txt_0.1.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -q -a1
if [ -d ./boot ] ; then
  mv ./boot/* .
  rm -rf boot
fi

%Build

%Install
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
cp -p * $RPM_BUILD_ROOT/%{pfx}/boot
if [ ! -e $RPM_BUILD_ROOT/%{pfx}/boot/start.elf ] ; then
  cp -p $RPM_BUILD_ROOT/%{pfx}/boot/arm240_start.elf $RPM_BUILD_ROOT/%{pfx}/boot/start.elf
fi 

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
