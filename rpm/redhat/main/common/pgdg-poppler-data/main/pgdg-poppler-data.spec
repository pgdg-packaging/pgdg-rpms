%global sname poppler-data
%global popplerdatainstdir /usr/%{name}

Name:		pgdg-%{sname}
Summary:	Encoding files for use with poppler
Version:	0.4.12
Release:	1%{?dist}

# NOTE: The licensing details are explained in COPYING file in source archive.
License:	BSD and GPLv2

URL:		https://poppler.freedesktop.org/
Source:		https://poppler.freedesktop.org/poppler-data-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	make
BuildRequires:	git

%if %{defined rhel} || %{defined centos}
#Patch200: example200.patch
%endif

%description
This package consists of encoding files for use with poppler. The encoding
files are optional and poppler will automatically read them if they are present.

When installed, the encoding files enables poppler to correctly render both CJK
and Cyrrilic characters properly.

%package	devel
Summary:	Devel files for %{name}

Requires:	%{name} = %{version}-%{release}
BuildRequires:	pkgconfig

%description devel
This sub-package currently contains only pkgconfig file, which can be used with
pkgconfig utility allowing your software to be build with poppler-data.

%prep
%autosetup -S git -n %{sname}-%{version}

# NOTE: Nothing to do here - we are packaging the content only.
%build

%install
%make_install prefix=%{popplerdatainstdir}

# Install pkgconfig file under standard directory:
%{__mkdir} -p %{buildroot}%{_libdir}/pkgconfig/
%{__mv} %{buildroot}%{popplerdatainstdir}/share/pkgconfig/poppler-data.pc %{buildroot}%{_libdir}/pkgconfig/pgdg-poppler-data.pc

%files
%license COPYING COPYING.adobe COPYING.gpl2
%{popplerdatainstdir}/share/poppler/

%files devel
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 0.4.12-1
- Update to 0.4.12 per changes described at:
  https://poppler.freedesktop.org/releases.html

* Wed May 19 2021 Devrim Gündüz <devrim@gunduz.org> - 0.4.9-7
- Initial packaging for PostgreSQL RPM repository, to prevent
  further breakages caused by Poppler updates on RHEL 8.x. Spec file taken
  from Fedora rawhide.
