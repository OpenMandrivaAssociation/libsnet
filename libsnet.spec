%define	major 0
%define libname	%mklibname snet %{major}

Summary:	The libsnet library
Name:		libsnet
Version:	20060320
Release:	%mkrel 3
License:	BSD
Group:		System/Libraries
URL:		http://sourceforge.net/projects/libsnet
Source0:	libsnet-%{version}.tar.bz2
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	openssl-devel
BuildRequires:	libsasl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
The libsnet library

%package -n	%{libname}
Summary:	The libsnet library
Group:          System/Libraries

%description -n	%{libname}
The libsnet library

%package -n	%{libname}-devel
Summary:	Static library and header files for the libsnet library
Group:		Development/C
Provides:	libsnet-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
This package contains the static libsnet library and its header
files needed to compile applications such as radmind, nefu, etc.

%prep

%setup -q -n libsnet

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
#export WANT_AUTOCONF_2_5=1
#rm -f configure
#libtoolize --copy --force; aclocal-1.7; autoconf

%configure2_5x \
    --enable-shared \
    --enable-static 

make OPTOPTS="%{optflags} -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la


