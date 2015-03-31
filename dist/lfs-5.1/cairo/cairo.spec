%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A 2D vectorial drawing library needed by GTK from 2.8.0
Name            : cairo
Version         : 1.4.10
Release         : 1
License         : LGPL or MPL 1.1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
URL             : http://cairographics.org/
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
XTRA_OPTS="--disable-win32"

if [ "$PKG_CAIRO_WANT_DIRECTFB" = "y" ]
then
    XTRA_OPTS="$XTRA_OPTS --enable-directfb"
fi

if [ "$PKG_CAIRO_WANT_PDF" != "y" ]
then
    XTRA_OPTS="$XTRA_OPTS --disable-pdf"
fi

if [ "$PKG_CAIRO_WANT_PS" != "y" ]
then
    XTRA_OPTS="$XTRA_OPTS --disable-ps"
fi

if [ "$PKG_CAIRO_WANT_SVG" != "y" ]
then
    XTRA_OPTS="$XTRA_OPTS --disable-svg"
fi

if [ "$PKG_CAIRO_WANT_XLIB" != "y" ]
then
    XTRA_OPTS="$XTRA_OPTS --disable-xlib"
fi

./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} $XTRA_OPTS
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
