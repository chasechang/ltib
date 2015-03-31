# Template = kernel-common.tmpl

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : XFS utilities
Name            : xfsprogs
Version         : 2.8.18
Release         : 1
License         : GPL
Vendor          : Open source
Packager        : Michael Reiss
Group           : System Environment/Kernel
Source          : %{name}-%{version}-%{release}.tar.gz
Patch1          : xfsprogs-2.8.18-fix-abs-symlinks.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
./configure --prefix=%{_prefix} --bindir=%{_prefix}/sbin --host=$CFGHOST --build=%{_build} PLATFORM=linux
make

%Install
DIST_ROOT=$RPM_BUILD_ROOT/%{pfx}
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV
make install DIST_MANIFEST=$DIST_INSTALL
make -C build/rpm rpmfiles DIST_MANIFEST=$DIST_INSTALL
make install-dev DIST_MANIFEST=$DIST_INSTALL_DEV
make -C build/rpm rpmfiles-dev DIST_MANIFEST=$DIST_INSTALL_DEV
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
