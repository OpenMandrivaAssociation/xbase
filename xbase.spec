%define name	xbase
%define version 3.1.2
%define major 1
%define libname %mklibname %name %major
%define libnamedev %mklibname -d %name 

Summary:	Xbase dBase database file library
Name: 		%{name}
Version:	%{version}
Release: 	%mkrel 4
Source:		http://downloads.sourceforge.net/xdb/%{name}64-%{version}.tar.gz
Patch0:		xbase-3.1.2-fixconfig.patch
Patch1:		xbase-3.1.2-gcc44.patch
Patch2:		xbase-2.0.0-ppc.patch
Patch3:		xbase-3.1.2-xbnode.patch
License:	LGPLv2+
Group: 		Development/Other
URL:		http://linux.techass.com/projects/xdb/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	doxygen
BuildRequires:	multiarch-utils

%description
Library for accessing dBase .dbf, .ndx, .dbt, and Clipper .ntx files.

%package -n %{libname}
Summary: Libraries needed for %{name}
Group:   System/Libraries
Provides: lib%{name} = %version-%release

%description -n %{libname}
Libraries needed for %{name}

%package -n %{libnamedev}
Summary: Xbase development package
Group: Development/Other
Requires: %{libname} = %version
Provides: %name-devel = %version-%release
Obsoletes: %{name}-devel < 2.0.0-8mdv
Obsoletes: %{libname}-devel < 2.0.0-8mdv
Conflicts: %{name} < 3.1.2-4

%description -n %{libnamedev}
Headers and such for compiling programs that use the Xbase library.

%prep
%setup -qn %{name}64-%{version}
%patch0 -p1
%patch1 -p1 -b .gcc44
%patch2 -p1
%patch3 -p1

%build
touch AUTHORS README NEWS
cp -p copying COPYING
autoreconf -i
%configure2_5x --disable-static
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

pushd $RPM_BUILD_ROOT%{_libdir}
ln -s libxbase64.so.1.0.0 libxbase.so.1.0.0
ln -s libxbase64.so.1 libxbase.so.1
ln -s libxbase64.so libxbase.so
popd

pushd $RPM_BUILD_ROOT%{_includedir}
ln -s xbase64 xbase
ln -s xbase64.h xbase64/xbase.h
popd

pushd $RPM_BUILD_ROOT%{_bindir}
ln -s xbase64-config xbase-config
popd

%multiarch_binaries %{buildroot}%{_bindir}/xbase64-config

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig 
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc NEWS README AUTHORS ChangeLog
%{_bindir}/checkndx
%{_bindir}/copydbf
%{_bindir}/dbfutil1
%{_bindir}/dbfxtrct
%{_bindir}/deletall
%{_bindir}/dumphdr
%{_bindir}/dumprecs
%{_bindir}/packdbf
%{_bindir}/reindex
%{_bindir}/undelall
%{_bindir}/zap

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%pre -n %{libnamedev}
if [ "$1" == "2" -a -d %{_includedir}/xbase ]
then
	rm -fr %{_includedir}/xbase
fi

%files -n %{libnamedev}
%defattr(-,root,root,-)
%doc docs html
%{_bindir}/xbase-config
%{_bindir}/xbase64-config
%{multiarch_bindir}/xbase64-config
%{_includedir}/xbase*
%{_libdir}/*.so
