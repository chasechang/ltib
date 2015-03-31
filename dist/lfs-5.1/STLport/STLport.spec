%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Multiplatform C++ Standard Library (STL implementation)
Name            : STLport
Version         : 5.2.1
Release         : 1
License         : STLport License (BSD style)
Vendor          : Zee2 Ltd
Packager        : Stuart Hughes
Group           : Applications/System
URL             : http://sourceforge.net/projects/stlport/files/STLport/STLport-5.2.1/
Source          : %{name}-%{version}.tar.gz
Patch1          : STLport-5.2.1-install.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
OPT_CFGHOST=`echo ${TOOLCHAIN_PREFIX} | perl -n -e 's,-$,,;print'`
./configure --prefix=%{_prefix} \
    --with-extra-cxxflags="-D_STLP_NO_VENDOR_STDLIB_L -D_STLP_NO_NATIVE_WIDE_FUNCTIONS" \
    --with-extra-cflags="-D_STLP_NO_VENDOR_STDLIB_L -D_STLP_NO_NATIVE_WIDE_FUNCTIONS"
make release-shared

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
make -j1 install-release-shared DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
