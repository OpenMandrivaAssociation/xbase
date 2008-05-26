%define name	xbase
%define version 2.0.0
%define major 2
%define libname %mklibname %name %major
%define libnamedev %mklibname -d %name 


Summary:	Xbase dBase database file library
Name: 		%{name}
Version:	%{version}
Release: 	%mkrel 8
Source: 	%{name}-%{version}.tar.bz2
# (fc) 2.0.0-8mdv fix build with gcc 4.3 (Fedora)
Patch0:		xbase-2.0.0-gcc43.patch
# (fc) 2.0.0-8mdv fix xbase-config --ld (RH bug #162845) (Fedora)
Patch1:		xbase-2.0.0-fixconfig.patch
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

%package -n %{libnamedev}
Summary: Xbase development package
Group: Development/Other
Requires: %{libname} = %version
Provides: %name-devel = %version-%release
Obsoletes: %{name}-devel < 2.0.0-8mdv
Obsoletes: %{libname}-devel < 2.0.0-8mdv

%description -n %{libnamedev}
Headers and such for compiling programs that use the Xbase library.

%prep
%setup -n %{name}-%{version} -q
%patch0 -p1 -b .gcc43
%patch1 -p1 -b .fixconfig


%build
%configure2_5x --disable-static
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc NEWS README TODO AUTHORS COPYING ChangeLog
%{_bindir}/*
%exclude %{_bindir}/xbase-config

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root,-)
%doc docs html
%{_bindir}/xbase-config
%{_includedir}/xbase
%{_libdir}/*.so
%{_libdir}/*.la
