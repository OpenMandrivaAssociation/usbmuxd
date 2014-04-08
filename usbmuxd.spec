%define major		2
%define libname		%mklibname %{name} %{major}
%define libnamedev	%mklibname %{name} -d

Name:		usbmuxd
Version:	1.0.9
Release:	1
Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Group:		System/Kernel and hardware 
License:	GPLv2+ and LGPLv2+
URL:		http://www.libimobiledevice.org/
Source0:	http://www.libimobiledevice.org/downloads/lib%{name}-%{version}.tar.bz2

BuildRequires:	libtool
BuildRequires:	pkgconfig(libplist) >= 1.11

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

#---------------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Library to access the usbmuxd daemon
Group:		System/Libraries
Requires:	%{name} >= %{version}-%{release}

%description -n %{libname}
libusmuxd is used to communicate with the usbmuxd daemon by apps wishing to 
interact with Apple's iPod Touch and iPhone.

#---------------------------------------------------------------------------------

%package -n	%{libnamedev}
Summary:	Development package for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libnamedev}
Files for development with %{name}.

#---------------------------------------------------------------------------------
%prep
%setup -q -n lib%{name}-%{version}

%build
autoreconf -vfi
%configure2_5x \
		--disable-static
%make

%install
%makeinstall_std

# we don't want these
find %{buildroot} -name '*.la' -delete

%pre
%_pre_useradd usbmux /proc /sbin/nologin

%postun
%_postun_userdel usbmux

%files
%doc AUTHORS README
%{_bindir}/iproxy

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}.so.%{major}.*

%files -n %{libnamedev}
%doc README
%{_includedir}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
