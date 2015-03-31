%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : thttpd (tiny/turbo/throttling HTTP server) is an open source software web server from ACME Laboratories.
Name            : lighttpd
Version         : 1.4.26
Release         : 0
License         : BSD
Vendor          : Adtec Digital
Packager        : Mike Goins
Group           : System Environment/Daemons
URL             : http://www.lighttpd.net/
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}
   
%Prep
%setup 

%Build
ac_cv_path_PCRECONFIG=$DEV_IMAGE/usr/bin/pcre-config \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
