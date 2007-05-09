%define name	xbase
%define version 2.0.0
%define release 5mdk
%define major 2
%define libname %mklibname %name %major


Summary:	Xbase dBase database file library
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
Source: 	%{name}-%{version}.tar.bz2
License:	LGPL
Group: 		Development/Other
URL:		http://linux.techass.com/projects/xdb/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  libstdc++-devel


%undefine __check_files

%description
Library for accessing dBase .dbf, .ndx, .dbt, and Clipper .ntx files.

%package -n %{libname}
Summary: Libraries needed for %{name}
Group:   System/Libraries
Provides: lib%{name} = %version-%release

%description -n %{libname}
Libraries needed for %{name}

%package -n %{libname}-devel
Summary: Xbase development package
Group: Development/Other
Requires: %{libname} = %version
Provides: %name-devel = %version-%release
Provides: lib%{name}-devel = %version-%release
Obsoletes: %{name}-devel < %version-%release

%description -n %{libname}-devel
Headers and such for compiling programs that use the Xbase library.

%prep
%setup -n %{name}-%{version} -q

%build
%{?__cputoolize:%{__cputoolize}}
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --libdir=%{_libdir} --enable-static
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -rf $RPM_BUILD_ROOT/%{_bindir}/xbase-config

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig 

%post -n %{libname}-devel -p /sbin/ldconfig
%postun -n %{libname}-devel -p /sbin/ldconfig 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc NEWS README TODO AUTHORS COPYING ChangeLog
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libxbase-2.0.so.*

%files -n %{libname}-devel
%defattr(-,root,root,-)
%doc docs html
%{_includedir}/xbase
%{_libdir}/libxbase.so
%{_libdir}/libxbase.la
%{_libdir}/libxbase.a
