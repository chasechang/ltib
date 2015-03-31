%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : IPSec VPN client compatible with Cisco equipment
Name            : vpnc
Version         : 0.5.3
Release         : 2
License         : GPLv2+
Vendor          : UNKNOWN(LTIB addsrpms)
Packager        : UNKNOWN(LTIB addsrpms)
Group           : Applications/Internet
URL             : http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:        http://www.unix-ag.uni-kl.de/~massar/vpnc/vpnc-0.5.3.tar.gz
Source1:        generic-vpnc.conf
Source2:	vpnc.consolehelper
Source3:	vpnc-disconnect.consolehelper
Source4:	vpnc.pam
Source5:	vpnc-helper
Source6:	vpnc-cleanup
Patch2:		vpnc-0.5.3-cloexec.patch
Patch3:		vpnc-0.5.1-dpd.patch
Patch4:		vpnc-makeman-cross.patch

BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms vpnc-0.5.3-2.fc10.src.rpm

%Prep

%setup -q
%patch2 -p1
%patch3 -p1
%patch4 -p0


%Build
if ! type libgcrypt-config
then
    cat <<TXT

vpnc requires the script libgcrypt-config on the host.
Please install this using your package manager.
On Debian/Ubuntu this is in libgcryp11-dev.

TXT
    exit 1
fi

make PREFIX=/usr 


%Install
rm -rf $RPM_BUILD_ROOT/%{pfx}/
make install DESTDIR="$RPM_BUILD_ROOT/%{pfx}/" PREFIX=/usr
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_bindir}/pcf2vpnc
chmod 0644 pcf2vpnc
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man1/pcf2vpnc.1
chmod 0644 $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man8/vpnc.8
install -m 0600 %{SOURCE1} $RPM_BUILD_ROOT/%{pfx}/%{_sysconfdir}/vpnc/default.conf
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_var}/run/vpnc
touch $RPM_BUILD_ROOT/%{pfx}/%{_var}/run/vpnc/pid \
      $RPM_BUILD_ROOT/%{pfx}/%{_var}/run/vpnc/defaultroute \
      $RPM_BUILD_ROOT/%{pfx}/%{_var}/run/vpnc/resolv.conf-backup
install -Dp -m 0644 %{SOURCE2} \
    $RPM_BUILD_ROOT/%{pfx}/%{_sysconfdir}/security/console.apps/vpnc
install -Dp -m 0644 %{SOURCE3} \
    $RPM_BUILD_ROOT/%{pfx}/%{_sysconfdir}/security/console.apps/vpnc-disconnect
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT/%{pfx}/%{_sysconfdir}/pam.d/vpnc
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT/%{pfx}/%{_sysconfdir}/pam.d/vpnc-disconnect
install -m 0755 %{SOURCE5} \
    $RPM_BUILD_ROOT/%{pfx}/%{_sbindir}/vpnc-helper
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_bindir}
ln -sf consolehelper $RPM_BUILD_ROOT/%{pfx}/%{_bindir}/vpnc
ln -sf consolehelper $RPM_BUILD_ROOT/%{pfx}/%{_bindir}/vpnc-disconnect
install -Dp -m 0644 %{SOURCE6} \
    $RPM_BUILD_ROOT/%{pfx}/%{_sysconfdir}/event.d/vpnc-cleanup
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_datadir}/doc/vpnc/COPYING


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
