%define major 2
%define libname %mklibname usbmuxd %{major}
%define develname %mklibname -d usbmuxd

Name:		usbmuxd
Version:	1.0.8
Release:	8
Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://marcansoft.com/blog/iphonelinux/usbmuxd/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
Patch0:		usbmux_udev_owner_fix.patch

BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libplist)
BuildRequires:	cmake

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%package -n %{libname}
Group:		System/Libraries
Summary:	Library to access the usbmuxd daemon
Obsoletes:	%{mklibname usbmuxd 1} <= 1.0.7

%description -n %{libname}
libusmuxd is used to communicate with the usbmuxd daemon by apps wishing to 
interact with Apple's iPod Touch and iPhone.

%package -n %{develname}
Summary:	Development package for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Files for development with %{name}.

%prep
%setup -q

%build
%cmake -DUSB_INCLUDE_DIR=%{_includedir}/libusb-1.0
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

%files -n %{libname}
%{_libdir}/libusbmuxd.so.%{major}*
%{_libdir}/libusbmuxd.so.%{version}


%files -n %{develname}
%doc README.devel
%{_includedir}/*.h
%{_libdir}/libusbmuxd.so
%{_libdir}/pkgconfig/libusbmuxd.pc


%changelog
* Tue Apr 17 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.0.8-1
+ Revision: 791416
- version update 1.0.8

* Fri Feb 24 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.0.7-3
+ Revision: 780183
- Fix bug #65298

* Tue Dec 06 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.0.7-2
+ Revision: 738450
- rebuild
- cleaned up spec
- removed mkrel, BuildRoot, clean section, defattr
- removed dep LOOP
- removed old ldconfig scriptlets

* Thu Apr 14 2011 Götz Waschk <waschk@mandriva.org> 1.0.7-1
+ Revision: 652993
- new version
- drop patch

* Sun Nov 28 2010 Funda Wang <fwang@mandriva.org> 1.0.6-2mdv2011.0
+ Revision: 602257
- update BR
- update produce id
- new version 1.0.6

* Thu Jul 22 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.0.5-2mdv2011.0
+ Revision: 556924
- add libplist build requires

* Thu Jul 22 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.0.5-1mdv2011.0
+ Revision: 556886
- usbmuxd 1.0.5

* Wed May 12 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.0.4-1mdv2010.1
+ Revision: 544554
- usbmuxd 1.0.4

* Mon Apr 12 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.0.3-2mdv2010.1
+ Revision: 533666
- fix patch0: apply the ACLs on the usb device node before trying to access it (was broken during the 1.0.3 rediff)

* Mon Mar 22 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.0.3-1mdv2010.1
+ Revision: 526416
- rediff ACL patch
- usbmuxd 1.0.3

* Thu Feb 11 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.0.2-1mdv2010.1
+ Revision: 504139
- usbmuxd 1.0.2

* Mon Dec 07 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.0.0-3mdv2010.1
+ Revision: 474470
- need to actually upload libplist before attempting the rebuild ;)

* Mon Dec 07 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.0.0-2mdv2010.1
+ Revision: 474467
- rebuilg against new libplist

* Mon Dec 07 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.0.0-1mdv2010.1
+ Revision: 474344
- usbmuxd 1.0.0

* Fri Nov 06 2009 Colin Guthrie <cguthrie@mandriva.org> 1.0.0-0.rc2.1mdv2010.1
+ Revision: 460546
- New version: 1.0.0-rc2 (work by teuf)
- Add usbmux user
- Add ACL for usbmux user
- Apply upstream patches for smooth exit.

* Mon Sep 14 2009 Götz Waschk <waschk@mandriva.org> 0.1.4-2mdv2010.0
+ Revision: 439806
- rebuild for new libusb

* Mon Aug 10 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.1.4-1mdv2010.0
+ Revision: 414335
- 0.1.4
- usbmuxd 0.1.4

* Thu Aug 06 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.1.3-1mdv2010.0
+ Revision: 410626
- Fix rpm groups
- import usbmuxd

