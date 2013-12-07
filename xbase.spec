%define name	xbase
%define version 3.1.2
%define major 1
%define libname %mklibname %name %major
%define libnamedev %mklibname -d %name 

Summary:	Xbase dBase database file library
Name: 		%{name}
Version:	%{version}
Release: 	10
Source0:	http://downloads.sourceforge.net/xdb/%{name}64-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch0:		%{name}-%{version}-fixconfig.patch
Patch2:		%{name}-%{version}-gcc44.patch
Patch3:		%{name}-2.0.0-ppc.patch
Patch4:		%{name}-%{version}-xbnode.patch
Patch5:		%{name}-%{version}-lesserg.patch
Patch6:		%{name}-%{version}-outofsource.patch
Patch7:		%{name}-%{version}-gcc47.patch
Patch8:		%{name}-%{version}-gcc-version.patch
Patch9:		xbase-automake-1.13.patch

License:	LGPLv2+
Group: 		Development/Other
URL:		http://linux.techass.com/projects/xdb/
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
%apply_patches


%build
touch AUTHORS README NEWS
cp -p copying COPYING
autoreconf -i
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_libdir}/*.la

pushd %{buildroot}%{_libdir}
ln -s libxbase64.so.1.0.0 libxbase.so.1.0.0
ln -s libxbase64.so.1 libxbase.so.1
ln -s libxbase64.so libxbase.so
popd

pushd %{buildroot}%{_includedir}
ln -s xbase64 xbase
ln -s xbase64.h xbase64/xbase.h
popd

pushd %{buildroot}%{_bindir}
ln -s xbase64-config xbase-config
popd

%multiarch_binaries %{buildroot}%{_bindir}/xbase64-config

%files
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
%{_libdir}/*.so.*

%pre -n %{libnamedev}
if [ "$1" == "2" -a -d %{_includedir}/xbase ]
then
	rm -fr %{_includedir}/xbase
fi

%files -n %{libnamedev}
%doc docs html
%{_bindir}/xbase-config
%{_bindir}/xbase64-config
%{multiarch_bindir}/xbase64-config
%{_includedir}/xbase*
%{_libdir}/*.so
