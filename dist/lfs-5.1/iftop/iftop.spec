%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : iftop - display bandwidth usage on an interface by host
Name            : iftop
Version         : 0.17
Release         : 1
License         : GPL
Vendor          : Zee2
Packager        : Stuart Hughes
Group           : Development/Tools
URL             : http://www.ex-parrot.com/pdw/iftop/
Source          : http://www.ex-parrot.com/pdw/iftop/download/%{name}-%{version}.tar.gz
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
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
