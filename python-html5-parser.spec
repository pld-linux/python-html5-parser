#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module html5-parser
Summary:	A fast, standards compliant, C based, HTML 5 parser for python
Name:		python-%{module}
Version:	0.4.5
Release:	4
# html5-parser-0.4.4/gumbo/utf8.c is MIT
License:	ASL 2.0 and MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/h/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	0d133a1f6d8251f5a786df5074423e29
URL:		https://pypi.python.org/pypi/%{module}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	python-chardet
BuildRequires:	python-bs4
BuildRequires:	python-lxml >= 3.8.0
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-devel
BuildRequires:	python3-bs4
BuildRequires:	python3-setuptools
BuildRequires:	python3-chardet
BuildRequires:	python3-lxml >= 3.8.0
%endif
BuildRequires:	sed >= 4.0
# replace with other requires if defined in setup.py
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A fast, standards compliant, C based, HTML 5 parser for python

%package -n python3-%{module}
Summary:	A fast, standards compliant, C based, HTML 5 parser for python
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
A fast, standards compliant, C based, HTML 5 parser for python

%prep
%setup -q -n %{module}-%{version}

# remove shebangs from library files
%{__sed} -i -e '/^#!\//, 1d' src/html5_parser/*.py

%{__sed} -i -e '/extra_compile_args=cargs,/d' setup.py

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files -n python-%{module}
%defattr(644,root,root,755)
%doc README.rst
%dir %{py_sitedir}/html5_parser
%{py_sitedir}/html5_parser/*.py[co]
%attr(755,root,root) %{py_sitedir}/html5_parser/*.so
%{py_sitedir}/html5_parser-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/html5_parser
%{py3_sitedir}/html5_parser/*.py
%attr(755,root,root) %{py3_sitedir}/html5_parser/*.so
%{py3_sitedir}/html5_parser/__pycache__
%{py3_sitedir}/html5_parser-%{version}-py*.egg-info
%endif
