%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Avahi mDNS/DNS-SD service discovery suite
Name            : avahi
Version         : 0.6.30
Release         : 2
License         : LGPL
Vendor          : Avid Technology
Packager        : Fritz Mueller
Group           : System/Daemons
URL             : http://avahi.org
Source          : %{name}-%{version}.tar.gz
Patch1          : avahi-0.6.30-ipv4ll.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build

XTRA_OPTS=""

if [ "$PKG_AVAHI_WANT_AUTOIPD" = "y" ]
then
    XTRA_OPTS="$XTRA_OPTS --enable-autoipd --with-autoipd-user=avahi --with-autoipd-group=avahi"
else
    XTRA_OPTS="$XTRA_OPTS --disable-autoipd"
fi

./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --with-distro=debian --disable-nls --disable-glib --disable-gobject --disable-qt3 --disable-qt4 --disable-gtk --disable-gtk3 --disable-gdbm --disable-mono --disable-monodoc --disable-python --disable-doxygen-doc --disable-manpages --enable-compat-libdns_sd --localstatedir=/var $XTRA_OPTS
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
