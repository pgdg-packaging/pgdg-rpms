%global sname faker
%global _description\
Faker is a Python package that generates fake data for you. Whether you need\
to bootstrap your database, create good-looking XML documents, fill-in your\
persistence to stress test it, or anonymize data taken from a production\
service, Faker is for you.

Name:		python3-%{sname}
Version:	40.37.0
Release:	1%{?dist}
Summary:	Faker is a Python package that generates fake data for you

License:	MIT
URL:		https://faker.readthedocs.io
Source:		https://github.com/joke2k/%{sname}/archive/v%{version}/%{sname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools

%description %_description

%package doc
Summary:	Documentation for %{name}

%description doc %_description

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{sname}
%license LICENSE.txt
%{_bindir}/faker
%{python3_sitelib}/%{sname}
%{python3_sitelib}/Faker-%{version}-py*.egg-info

%files doc
%license LICENSE.txt
%doc README.rst CHANGELOG.md CONTRIBUTING.rst RELEASE_PROCESS.rst docs/*.rst

%changelog
* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 40.37.0-1
- Update to 40.37.0 per changes described at:
  https://github.com/joke2k/faker/releases/tag/v40.37.0

* Wed Feb 10 2021 Juan Orti Alcaine <jortialc@redhat.com> - 6.1.1-1
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  postgresql_faker extension dependency on RHEL 7 and 8.
