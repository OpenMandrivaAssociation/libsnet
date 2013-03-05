%define	major	0
%define libname %mklibname snet %{major}
%define libp	%mklibname snet_p %{major}
%define devname %mklibname snet -d

Summary:	The libsnet library
Name:		libsnet
Version:	20070618
Release:	6
License:	BSD
Group:		System/Libraries
Url:		http://sourceforge.net/projects/libsnet
Source0:	%{name}-%{version}.tar.gz
Patch0:		libsnet-makefile_fixes.diff

BuildRequires:	libtool
BuildRequires:	libsasl-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)

%description
The libsnet library

%package -n	%{libname}
Summary:	The libsnet library
Group:          System/Libraries

%description -n	%{libname}
The libsnet library

%package -n	%{libp}
Summary:	The libsnet library
Group:          System/Libraries
Conflicts:	%{_lib}snet0 < 20070618-6

%description -n	%{libp}
The libsnet library

%package -n	%{devname}
Summary:	Development library and header files for the libsnet library
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{libp} = %{version}
Provides:	snet-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development libsnet library and its header
files needed to compile applications such as radmind, nefu, etc.

%prep
%setup -qn libsnet
%patch0 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# lib64 fixes
sed -i -e "s|/lib\b|/%{_lib}|g" *

%build
export OPTOPTS="%{optflags} -fPIC"
export LIBS="-lcrypto -lssl -lsasl2 -lz"

%configure2_5x \
	--enable-shared \
	--disable-static \
	--with-zlib=%{_prefix} \
	--with-ssl=%{_prefix} \
	--with-sasl=%{_prefix}

make 

%install
%makeinstall

%files -n %{libname}
%{_libdir}/libsnet.so.%{major}*

%files -n %{libp}
%{_libdir}/libsnet_p.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so

