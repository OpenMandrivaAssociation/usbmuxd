%define	git	20211124

Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Name:		usbmuxd
Version:	1.1.2
Release:	0.%{git}.1
Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://www.libimobiledevice.org/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.xz
Source1:	%{name}.sysusers
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libplist-2.0) >= 2.2.0
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-rpm-macros
BuildRequires:	pkgconfig(libimobiledevice-1.0)
Requires(pre):	systemd
%systemd_requires

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%prep
%autosetup -p1

%build
./autogen.sh
%configure --with-udevrulesdir="%{_udevrulesdir}"
%make_build

%install
%make_install

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-usbmuxd.preset << EOF
enable usbmuxd.service
EOF

install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

%pre
%sysusers_create_package %{name}.conf %{SOURCE1}

%preun
%systemd_preun usbmuxd.service

%post
%systemd_post usbmuxd.service

%postun
%systemd_postun_with_restart usbmuxd.service

%files
%doc AUTHORS
%{_udevrulesdir}/39-usbmuxd.rules
%{_presetdir}/86-usbmuxd.preset
%{_unitdir}/usbmuxd.service
%{_sbindir}/usbmuxd
%{_mandir}/man8/usbmuxd.8.*
%{_sysusersdir}/%{name}.conf
