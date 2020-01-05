Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Name:		usbmuxd
Version:	1.1.0
Release:	7
Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://www.libimobiledevice.org/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libplist) >= 1.1
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-macros
BuildRequires:  pkgconfig(libimobiledevice-1.0)
Requires(pre,postun):	rpm-helper
BuildRequires:		rpm-helper

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%prep
%setup -q

%build
%configure --with-udevrulesdir="/lib/udev/rules.d/"
%make

%install
%makeinstall_std

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-usbmuxd.preset << EOF
enable usbmuxd.service
EOF

%pre
%_pre_useradd usbmux /proc /sbin/nologin

%postun
%_postun_userdel usbmux

%files
%doc AUTHORS README
/lib/udev/rules.d/39-usbmuxd.rules
%{_presetdir}/86-usbmuxd.preset
%{_unitdir}/usbmuxd.service
%{_sbindir}/usbmuxd
%{_mandir}/man1/usbmuxd.1.*
