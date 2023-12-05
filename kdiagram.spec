%define major 6
%define devname %mklibname KGantt6 -d

Name: kdiagram
Version: 3.0.0
%define is_beta %(if test `echo %{version} |cut -d. -f3` -ge 70; then echo -n 1; else echo -n 0; fi)
%if %{is_beta}
%define ftpdir unstable
%else
%define ftpdir stable
%endif
Release: 1
Source0: http://download.kde.org/%{ftpdir}/%{name}/%{version}/%{name}-%{version}.tar.xz
Summary: KDE library for gantt charts
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake(ECM)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(KPim6Libkdepim)
BuildRequires: cmake(Qt6PrintSupport)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6Sql)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: sasl-devel
BuildRequires: doxygen
BuildRequires: qt6-qttools-assistant

%description
KDE library for gantt charts.

%libpackage KChart6 3
%libpackage KGantt6 3

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{name} = %{EVRD}
Requires: %{mklibname KChart6} = %{EVRD}
Requires: %{mklibname KGantt6} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%autosetup -p1

%build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja
cd ../
%ninja -C build

%install
%ninja_install -C build

( cd %{buildroot}
find .%{_datadir}/locale -name "*.qm" |while read r; do
	LNG=`echo $r |cut -d/ -f5`
	echo "%%lang($LNG) `echo $r |cut -b2-`"
done ) >%{name}.lang

%files -f %{name}.lang

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/*
%{_qtdir}/mkspecs/modules/*.pri
