%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A file compression utility.
Name            : bzip2
Version         : 1.0.2
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/File
Source          : bzip2-1.0.2.tar.gz 
Patch0          : bzip2-1.0.2-notest.patch
Patch1          : bzip2-1.0.2-mandir.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p1

%Build
make -f Makefile-libbz2_so
make clean
make

%Install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
if [ "$PKG_BZIP2_WANT_SHARED" = "y" ]
then
   cp -a libbz2.so.1.0.2 ${RPM_BUILD_ROOT}/%{prefix}/usr/lib/
   ln -s libbz2.so.1.0.2 ${RPM_BUILD_ROOT}/%{prefix}/usr/lib/libbz2.so.1
   ln -s libbz2.so.1 ${RPM_BUILD_ROOT}/%{prefix}/usr/lib/libbz2.so
fi

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*


