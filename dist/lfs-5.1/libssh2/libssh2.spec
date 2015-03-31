%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : SSH2 client-side library
Name            : libssh2
Version         : 1.4.3
Release         : 1
License         : BSD License
Vendor          : Zee2 Ltd
Packager        : Stuart Hughes
Group           : Applications/System
URL             : http://www.libssh2.org/
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
