%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Skelleton files for an embedded root filesystem
Name            : skell
Version         : 1.19
Release         : 3
License         : GPL
Vendor          : Freescale
Packager        : Steve Papacharalambous/Stuart Hughes
Group           : System Environment/Utilities
Source          : %{name}-%{version}.tar.gz
Patch1          : skell-1.19-ipautoconf.patch
Patch2          : skell-1.19-avahi-dbus.patch
Patch3          : skell-1.19-ipv4ll.patch
Patch4          : skell-1.19-settime.patch
Patch5          : skell-1.19-devshmdir.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%Build

%Install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/%{pfx} install
if [ -z "$PKG_SKELL_WANT_TERMINFO" ]
then
    rm -rf $RPM_BUILD_ROOT/%{pfx}/usr/share/terminfo
fi
if [ "$PKG_NSS_MDNS" = "y" ]
then
    sed -i 's/hosts:.*/hosts:      files mdns4_minimal [NOTFOUND=return] dns mdns4/' $RPM_BUILD_ROOT/%{pfx}/etc/nsswitch.conf
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%attr(0666, root, root) %dev(c, 5, 0) %{pfx}/dev/tty
%attr(0600, root, root) %dev(c, 5, 1) %{pfx}/dev/console
%attr(0666, root, root) %dev(c, 1, 3) %{pfx}/dev/null
%attr(0755, root, root) %{pfx}/usr/bin/startx
%{pfx}/*
