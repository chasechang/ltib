%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary		: Second extended (ext2) filesystem and ext3 utilities
Name		: e2fsprogs
Version		: 1.41.4
Release		: 0
License		: GPL
Vendor		: Freescale
Packager	: Stuart Hughes, Emil Medve
Group		: System Environment/Base
URL		: http://e2fsprogs.sourceforge.net
Source		: %{name}-%{version}.tar.gz
Patch1          : e2fsprogs-1.41.4-fix-lib-links.patch
BuildRoot	: %{_tmppath}/%{name}
Prefix		: %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
if [ -n "$UCLIBC" ]
then
   extra_opts='--disable-tls'
fi
BUILD_CC=$BUILDCC ./configure --host=$CFGHOST --enable-elf-shlibs $extra_opts
make

%Install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/%{pfx} install install-libs

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-, root, root)
%{pfx}/*
