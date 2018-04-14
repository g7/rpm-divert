Name:           rpm-divert
Version:        0.0.1
Release:        1
Summary:        dpkg-divert alternative for non-Debian based distros

License:        BSD-3-Clause
URL:            https://github.com/g7/rpm-divert

Source:         %{name}-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  python3-base

%description
%summary

%prep
%setup -q -n %{name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root %{buildroot}

mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
ln -sf /usr/share/rpm-divert/rpm-divert.py %{buildroot}/%{_bindir}/rpm-divert

%files
%doc README.md
/usr/share/rpm-divert
#/usr/lib/python*
%{_bindir}

%changelog
* Wed Apr 04 2018 Eugenio "g7" Paolantonio <me@medesimo.eu> - 0.0.1-1
- Initial release
