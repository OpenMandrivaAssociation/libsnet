%define	major 0
%define libname %mklibname snet %{major}
%define develname %mklibname snet -d

Summary:	The libsnet library
Name:libsnet
Version:	20070618
Release:	5
License:	BSD
Group:		System/Libraries
URL:		http://sourceforge.net/projects/libsnet
Source0:	libsnet-%{version}.tar.gz
Patch0:		libsnet-makefile_fixes.diff
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	pkgconfig(openssl)
BuildRequires:	libsasl-devel
BuildRequires:	pkgconfig(zlib)

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
export OPTOPTS="%{optflags} -fPIC"
export LIBS="-lcrypto -lssl -lsasl2 -lz"

%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-zlib=%{_prefix} \
    --with-ssl=%{_prefix} \
    --with-sasl=%{_prefix}

make 

%makeinstall

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif
find $RPM_BUILD_ROOT/%{_libdir} -name '*.la' -exec rm {} \;

%files -n %{libname}
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a



%changelog
* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 20070618-5mdv2011.0
+ Revision: 627797
- don't force the usage of automake1.7

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 20070618-4mdv2011.0
+ Revision: 609778
- rebuild

* Tue Apr 13 2010 Funda Wang <fwang@mandriva.org> 20070618-3mdv2010.1
+ Revision: 533753
- rebuild

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 20070618-2mdv2010.0
+ Revision: 429831
- rebuild

* Fri Jul 11 2008 Oden Eriksson <oeriksson@mandriva.com> 20070618-1mdv2009.0
+ Revision: 233752
- new'ish cvs snapshot
- fix linkage and devel package naming

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 20060523-3mdv2008.1
+ Revision: 129083
- kill re-definition of %%buildroot on Pixel's request

* Thu May 24 2007 Oden Eriksson <oeriksson@mandriva.com> 20060523-3mdv2008.0
+ Revision: 30705
- new snap (20060523)


* Sun Dec 10 2006 Oden Eriksson <oeriksson@mandriva.com> 20060320-3mdv2007.0
+ Revision: 94513
- rebuild
- Import libsnet

* Fri Mar 24 2006 Oden Eriksson <oeriksson@mandriva.com> 20060320-2mdk
- fix build

* Fri Mar 24 2006 Oden Eriksson <oeriksson@mandriva.com> 20060320-1mdk
- new snapshot (20060320)
- fix naming
- fix deps

* Fri May 13 2005 Oden Eriksson <oeriksson@mandriva.com> 20041106-3mdk
- fix naming
- rpmlint fixes
- fix build on x86_64

* Sat Nov 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 20041106-2mdk
- update %%description for the devel package

* Sat Nov 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 20041106-1mdk
- initial mandrake package

