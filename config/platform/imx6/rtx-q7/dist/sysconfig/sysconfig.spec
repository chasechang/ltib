%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : System configuration package
Name            : sysconfig
Version         : 1.2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep


%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc
touch $RPM_BUILD_ROOT/%{pfx}/etc/version


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
