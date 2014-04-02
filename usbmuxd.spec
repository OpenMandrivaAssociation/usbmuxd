%define snapshot 290314


Name:		usbmuxd
Version:	1.0.9
%if %snapshot
Release:	0.290314.1
Source0:	%name-%{snapshot}.tar.bz2
%else
Release:	1
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar
%endif
Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://marcansoft.com/blog/iphonelinux/usbmuxd/
Patch1:		0001-Use-systemd-to-start-usbmuxd.patch
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libplist) =>1.1
BuildRequires:	cmake
BuildRequires:	pkgconfig(systemd)
Requires(pre,postun):	rpm-helper

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%prep
%setup -q
%apply_patches

%build
%cmake -DUSB_INCLUDE_DIR=%{_includedir}/libusb-1.0
%make

%install
%makeinstall_std -C build

%pre
%_pre_useradd usbmux /proc /sbin/nologin

%post
%systemd_post usbmuxd.service

%postun
%systemd_preun usbmuxd.service
%_postun_userdel usbmux


%files
%doc AUTHORS README
/lib/udev/rules.d/85-usbmuxd.rules
%{_unitdir}/usbmuxd.service
%{_bindir}/iproxy
%{_sbindir}/usbmuxd
