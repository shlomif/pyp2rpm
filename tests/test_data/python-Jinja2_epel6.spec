# Created by pyp2rpm-3.2.2
%global pypi_name Jinja2

Name:           python-%{pypi_name}
Version:        2.8
Release:        1%{?dist}
Summary:        A small but fast and easy to use stand-alone template engine written in pure python

License:        BSD
URL:            http://jinja.pocoo.org/
Source0:        https://files.pythonhosted.org/packages/source/J/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-Babel >= 0.8
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
 
Requires:       python-MarkupSafe

%description
Jinja2 is a template engine written in pure Python. It provides a Django_
inspired nonXML syntax but supports inline expressions and an optional
sandboxed_ environment.Nutshell Here a small example of a Jinja template:: {%
extends 'base.html' %} {% block title %}Memberlist{% endblock %} {% block
content %} <ul> {% for user in users %} <li><a href"{{ user.url }}">{{
user.username }}</a></li> {%...


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# generate html docs 
sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%doc html README.rst
%{python2_sitelib}/jinja2
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info


%changelog
* Tue Mar 21 2017 Michal Cyprian <mcyprian@redhat.com> - 2.8-1
- Initial package.
