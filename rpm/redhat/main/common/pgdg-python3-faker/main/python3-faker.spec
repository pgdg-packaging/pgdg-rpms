%global sname faker
%if 0%{?rhel} == 8
# postgresql_faker runs in plpython3, which uses Python 3.6 on RHEL 8. 14.2.1
# is the last Faker release that supports it. The Epoch is needed because
# 40.37.0, built with Python 3.12 by mistake, reached the RHEL 8 repos:
%global __python3 /usr/bin/python3.6
%endif
%global _description\
Faker is a Python package that generates fake data for you. Whether you need\
to bootstrap your database, create good-looking XML documents, fill-in your\
persistence to stress test it, or anonymize data taken from a production\
service, Faker is for you.

Name:		python3-%{sname}
%if 0%{?rhel} == 8
Epoch:		1
Version:	14.2.1
%else
Version:	40.44.0
%endif
Release:	1PGDG%{?dist}
Summary:	Faker is a Python package that generates fake data for you

License:	MIT
URL:		https://faker.readthedocs.io
Source:		https://github.com/joke2k/%{sname}/archive/v%{version}/%{sname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%if 0%{?rhel} == 8
Requires:	python3-dateutil python3-typing-extensions
%endif

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
* Fri Oct 30 2026 Devrim Gunduz <devrim@gunduz.org> - 40.44.0-1PGDG
- Update to 40.44.0 per changes described at:
  https://github.com/joke2k/faker/releases/tag/v40.44.0
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/478
- RHEL 8: Use 14.2.1 and Python 3.6, with Epoch 1. postgresql_faker could not
  import 40.37.0, which was built with Python 3.12, from plpython3.

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 40.37.0-1
- Update to 40.37.0 per changes described at:
  https://github.com/joke2k/faker/releases/tag/v40.37.0

* Wed Feb 10 2021 Juan Orti Alcaine <jortialc@redhat.com> - 6.1.1-1
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  postgresql_faker extension dependency on RHEL 7 and 8.
