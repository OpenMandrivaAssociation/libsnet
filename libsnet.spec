%define major 0
%define libname %mklibname snet %{major}
%define libnamep %mklibname snet_p %{major}
%define devname %mklibname snet -d

Summary:	The libsnet library
Name:		libsnet
Version:	1.0.0
Release:	2
Epoch:		1
License:	BSD
Group:		System/Libraries
Url:		https://sourceforge.net/projects/libsnet
Source0:	%{name}-%{version}.tar.gz
Patch0:		libsnet-makefile_fixes.diff
BuildRequires:	sasl-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)

%description
The libsnet library.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	The libsnet library
Group:		System/Libraries

%description -n %{libname}
The libsnet library.

%files -n %{libname}
%{_libdir}/libsnet.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libnamep}
Summary:	The libsnet library
Group:		System/Libraries
Conflicts:	%{_lib}sname0 < 1:1.0.0

%description -n %{libnamep}
The libsnet library.

%files -n %{libnamep}
%{_libdir}/libsnet_p.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Static library and header files for the libsnet library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libnamep} = %{EVRD}
Provides:	snet-devel = %{EVRD}
Provides:	libsnet-devel = %{EVRD}

%description -n	%{devname}
This package contains the static libsnet library and its header
files needed to compile applications such as radmind, nefu, etc.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" *

%build
export OPTOPTS="%{optflags} -fPIC"
export LIBS="-lcrypto -lssl -lsasl2 -lz"

%configure2_5x \
	--enable-shared \
	--disable-static \
	--with-zlib=%{_prefix} \
	--with-ssl=%{_prefix} \
	--with-sasl=%{_prefix}

%make

%install
%makeinstall

