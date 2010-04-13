%define	major 0
%define libname %mklibname snet %{major}
%define develname %mklibname snet -d

Summary:	The libsnet library
Name:		libsnet
Version:	20070618
Release:	%mkrel 3
License:	BSD
Group:		System/Libraries
URL:		http://sourceforge.net/projects/libsnet
Source0:	libsnet-%{version}.tar.gz
Patch0:		libsnet-makefile_fixes.diff
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	openssl-devel
BuildRequires:	libsasl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The libsnet library

%package -n	%{libname}
Summary:	The libsnet library
Group:          System/Libraries

%description -n	%{libname}
The libsnet library

%package -n	%{develname}
Summary:	Static library and header files for the libsnet library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	snet-devel = %{version}-%{release}
Provides:	libsnet-devel = %{version}-%{release}
Obsoletes:	%{mklibname snet 0 -d}

%description -n	%{develname}
This package contains the static libsnet library and its header
files needed to compile applications such as radmind, nefu, etc.

%prep

%setup -q -n libsnet
%patch0 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" *

%build
#export WANT_AUTOCONF_2_5=1
#rm -f configure
#libtoolize --copy --force; aclocal-1.7; autoconf

export OPTOPTS="%{optflags} -fPIC"
export LIBS="-lcrypto -lssl -lsasl2 -lz"

%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-zlib=%{_prefix} \
    --with-ssl=%{_prefix} \
    --with-sasl=%{_prefix}

make 

%install
rm -rf %{buildroot}

%makeinstall

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
