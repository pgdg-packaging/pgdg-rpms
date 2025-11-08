%global pypi_name	typing_extensions

Name:		python3-typing-extensions
Version:	4.7.0
Release:	2PGDG%{?dist}
Summary:	Python Typing Extensions

License:	PSF-2.0
URL:		https://pypi.org/project/typing-extensions/
Source0:	https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-4.7.0.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-flit-core

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
The `typing_extensions` module serves two related purposes:

- Enable use of new type system features on older Python versions. For example,
  `typing.TypeGuard` is new in Python 3.10, but `typing_extensions` allows
  users on previous Python versions to use it too.
- Enable experimentation with new type system PEPs before they are accepted and
  added to the `typing` module.

`typing_extensions` is treated specially by static type checkers such as
mypy and pyright. Objects defined in `typing_extensions` are treated the same
way as equivalent forms in `typing`.

`typing_extensions` uses
[Semantic Versioning](https://semver.org/). The
major version will be incremented only for backwards-incompatible changes.
Therefore, it's safe to depend
on `typing_extensions` like this: `typing_extensions >=x.y, <(x+1)`,
where `x.y` is the first version that includes all features you need.

`typing_extensions` supports Python versions 3.7 and higher.

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files %{pypi_name}


%check
cd src
%{python3} -m unittest discover

%files -n python3-typing-extensions -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG.md
%doc README.md

%changelog
* Sat Nov 8 2023 Devrim Gündüz <devrim@gunduz.org> - 4.7.0-2PGDG
- Fix builds on SLES
- Add missing BRs

* Fri Jun 30 2023 Devrim Gündüz <devrim@gunduz.org> - 3.9.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support psycopg3
  RPM on RHEL 8 and SLES 15. RHEL 9 and Fedora already has this package.
