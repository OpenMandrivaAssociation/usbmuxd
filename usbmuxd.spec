%define name usbmuxd
%define major 0
%define libname %mklibname usbmuxd %major
%define libnamedev %mklibname -d usbmuxd

Name:		%{name}
Version:	0.1.4
Release:	%mkrel 1
Summary:	Daemon for communicating with Apple's iPod Touch and iPhone

Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://cgit.pims.selfip.net/usbmuxd/
Source0:	http://cgit.pims.selfip.net/%{name}/snapshot/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libusb-devel
BuildRequires:	automake autoconf libtool

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
%setup -q

%build
autoreconf -fi
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{a,la}
%makeinstall_std
# Install udev rules in the correct location
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d/
install -D -m0644 udev/85-usbmuxd.rules $RPM_BUILD_ROOT/lib/udev/rules.d/85-usbmuxd.rules

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS README COPYING
/lib/udev/rules.d/85-usbmuxd.rules
%{_bindir}/iproxy
%{_sbindir}/usbmuxd

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/libusbmuxd.so.*

%files -n %libnamedev
%defattr(-,root,root,-)
%doc README.devel
%{_includedir}/*.h
%{_libdir}/libusbmuxd.so
%{_libdir}/libusbmuxd*a
%{_libdir}/pkgconfig/libusbmuxd.pc

