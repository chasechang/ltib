%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : FastCGI development kit
Name            : fcgi
Version         : 2.4.0
Release         : 1
License         : Open Market
Vendor          : Adtec, Inc.
Packager        : Mike Goins
Group           : Development/Languages
URL             : http://www.fastcgi.com
Source          : http://www.fastcgi.com/dist/%{name}-%{version}.tar.gz
Patch1          : fcgi-2.4.0-header_inc.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}
An open extension to CGI that provides high performance for all Internet 
applications without any of the limitations of existing Web server APIs.

%Prep
%setup
%patch1 -p1 

%Build
CXXFLAGS="-g -O2 -L../libfcgi/.libs" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
perl -pi -e 's,^sys_lib_search_path_spec=.*,sys_lib_search_path_spec=,' libtool
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
