%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : DK-TS-KIT Demonstration Software
Name            : dktskit_demo
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Future Designs, Inc.
Packager        : Lysle E. Shields
Group           : System Environment/Utilities
URL             : http://www.teamfdi.com
Source          : dktskit_demo-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
make prefix=%{_prefix} DESTDIR=$RPM_BUILD_ROOT/${pfx}

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=%{_prefix} DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

