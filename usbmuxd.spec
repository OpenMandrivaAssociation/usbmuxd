%define snapshot 140414


Name:		usbmuxd
Version:	1.0.9
%if %snapshot
Release:	0.140414.2
Source0:	%name-%{snapshot}.tar.xz
%else
Release:	1
Source0:	http://www.libimobiledevice.org/downloads/%{name}.tar
%endif
Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://marcansoft.com/blog/iphonelinux/usbmuxd/
Patch1:		add_systemd_functionality.patch
Patch2:		client_c_segfault.patch
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libplist) =>1.1
BuildRequires:	pkgconfig(systemd)
BuildRequires:  pkgconfig(libimobiledevice-1.0)

Requires(pre,postun):	rpm-helper

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%prep
%setup -q
%apply_patches

%build

./autogen.sh
%configure2_5x
%make

%install
%makeinstall_std

%pre
%_pre_useradd usbmux /proc /sbin/nologin

%post
%systemd_post usbmuxd.service

%postun
%systemd_preun usbmuxd.service
%_postun_userdel usbmux


%files
%doc AUTHORS README
/lib/udev/rules.d/39-usbmuxd.rules
%{_unitdir}/usbmuxd.service
%{_sbindir}/usbmuxd
