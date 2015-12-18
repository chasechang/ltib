%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Base files for an embedded root filesystem
Name            : base-files
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Retronix
Packager        : Chase Chang
Group           : System Environment/Utilities
#Source          : %{name}-%{version}.tar.gz
#Patch1		: skell-1.16-udev.patch
#Patch2		: skell-1.13-depmod-modalias.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
#%setup

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}

cd $RPM_BUILD_ROOT/%{pfx}
# create the path 
for path in "bin" "boot" "dev" "etc" "home" "lib" "mnt" "opt" "proc" "root" "sbin" "sys" "tmp" "usr/bin" "usr/include" "usr/lib" "usr/local" "usr/sbin" "usr/share" "usr/src" "var"
do
	mkdir -p ${path}
done

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
#%attr(2777,root,ftp)  %{pfx}/var/ftp/pub
%attr(1777,root,root) %{pfx}/tmp
%attr(0666, root, root) %dev(c, 5, 0) %{pfx}/dev/tty
%attr(0666, root, root) %dev(c, 5, 1) %{pfx}/dev/console
%attr(0666, root, root) %dev(c, 1, 3) %{pfx}/dev/null
%{pfx}/*
