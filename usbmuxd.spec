%define name usbmuxd
%define major 1
%define libname %mklibname usbmuxd %major
%define libnamedev %mklibname -d usbmuxd
#define extraver rc2

Name:		%{name}
Version:	1.0.3
Release:	%mkrel 2
Summary:	Daemon for communicating with Apple's iPod Touch and iPhone

Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://marcansoft.com/blog/iphonelinux/usbmuxd/
Source0:	http://marcansoft.com/uploads/usbmuxd/%{name}-%{version}%{?extraver:-%{extraver}}.tar.bz2
Patch0:		usbmuxd-1.0.0-rc2-udev-usbmux-user-acl.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libusb-devel
BuildRequires:	cmake

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%package -n %libname
Group: System/Libraries
Summary: Library to access the usbmuxd daemon
Requires: %name >= %version

%description -n %libname
libusmuxd is used to communicate with the usbmuxd daemon by apps wishing to 
interact with Apple's iPod Touch and iPhone.

%package -n %libnamedev
Summary: Development package for %{name}
Group: Development/C
Requires: %libname = %version
Provides: %name-devel = %version-%release

%description -n %libnamedev
Files for development with %{name}.

%prep
%setup -q -n %{name}-%{version}%{?extraver:-%{extraver}}
%apply_patches

%build
%cmake
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

%clean
rm -rf %{buildroot}

%pre
%_pre_useradd usbmux /proc /sbin/nologin

%postun
%_postun_userdel usbmux

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS README
/lib/udev/rules.d/85-usbmuxd.rules
%{_bindir}/iproxy
%{_sbindir}/usbmuxd

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/libusbmuxd.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root,-)
%doc README.devel
%{_includedir}/*.h
%{_libdir}/libusbmuxd.so
%{_libdir}/pkgconfig/libusbmuxd.pc

