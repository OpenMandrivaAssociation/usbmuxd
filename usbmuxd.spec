%define major 2
%define libname %mklibname usbmuxd %major
%define develname %mklibname -d usbmuxd

Name:		usbmuxd
Version:	1.0.8
Release:	2
Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://marcansoft.com/blog/iphonelinux/usbmuxd/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
Patch0:		usbmux_udev_owner_fix.patch
Patch1:		0001-Use-systemd-to-start-usbmuxd.patch

BuildRequires:	usb1.0-devel >= 1.0.3
BuildRequires:	cmake
BuildRequires:	libplist-devel
BuildRequires:	systemd-units

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%package -n %{libname}
Group: System/Libraries
Summary: Library to access the usbmuxd daemon

%description -n %{libname}
libusmuxd is used to communicate with the usbmuxd daemon by apps wishing to 
interact with Apple's iPod Touch and iPhone.

%package -n %{develname}
Summary: Development package for %{name}
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname}
Files for development with %{name}.

%prep
%setup -q
%patch1 -p1

%build
%cmake
%make

%install
%makeinstall_std -C build

%pre
%_pre_useradd usbmux /proc /sbin/nologin

%postun
%_postun_userdel usbmux

%files
%doc AUTHORS README
/lib/udev/rules.d/85-usbmuxd.rules
%{_bindir}/iproxy
%{_sbindir}/usbmuxd
%{_unitdir}/usbmuxd.service

%files -n %{libname}
%{_libdir}/libusbmuxd.so.%{major}*
%{_libdir}/libusbmuxd.so.%{version}

%files -n %{develname}
%doc README.devel
%{_includedir}/*.h
%{_libdir}/libusbmuxd.so
%{_libdir}/pkgconfig/libusbmuxd.pc
