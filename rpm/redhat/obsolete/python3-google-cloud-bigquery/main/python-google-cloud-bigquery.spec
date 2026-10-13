%global library google-cloud-bigquery

Name:		python3-%{library}
Version:	1.24.0
Release:	3%{?dist}
Epoch:		1
Summary:	Google Cloud Client Library for Python
License:	ASL 2.0
URL:		https://github.com/googleapis/google-cloud-python

Source0:	https://github.com/googleapis/google-cloud-python/archive/bigquery-1.24.0.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools python3-pip python3-wheel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
Google Cloud Python Client

%prep
%autosetup -n google-cloud-python-bigquery-%{version}

%build
pushd bigquery
%pyproject_wheel
popd

%install
pushd bigquery
%pyproject_install
popd

%files
%license LICENSE
%{python3_sitelib}/google/cloud/bigquery
%{python3_sitelib}/google/cloud/bigquery_v2
%{python3_sitelib}/google_cloud_bigquery-%{version}*.pth
%{python3_sitelib}/google_cloud_bigquery-%{version}.dist-info/

%changelog
* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.24.0-3
- Switch to pyproject builds

* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.24.0-2
- Fix the structural spec bug

* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.24.0-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  bigquery_fdw dependency.
