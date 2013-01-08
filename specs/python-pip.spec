%if (! 0%{?rhel}) || 0%{?rhel} > 6
%global with_python3 1
%endif
%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global srcname pip

Name:           python-%{srcname}
Version:        1.2.1
Release:        2%{?dist}
Summary:        Pip installs packages.  Python3 packages.  An easy_install replacement

Group:          Development/Libraries
License:        MIT
URL:            http://www.pip-installer.org
Source0:        http://pypi.python.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-setuptools

%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.


%if 0%{?with_python3}
%package -n python3-pip
Summary:        Pip installs packages.  Python3 packages.  An easy_install replacement
Group:          Development/Libraries

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:  python3-setuptools

%description -n python3-pip
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}
%{__sed} -i '1d' pip/__init__.py

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# Change the name of the pip executable in order to not conflict with perl-pip
# https://bugzilla.redhat.com/show_bug.cgi?id=616399
mv %{buildroot}%{_bindir}/pip %{buildroot}%{_bindir}/python3-pip

# after changing the pip-python binary name, make a symlink to the old name,
# that will be removed in a later version
# https://bugzilla.redhat.com/show_bug.cgi?id=855495
pushd %{buildroot}%{_bindir}
ln -s python3-pip pip-python3
popd

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Remove the extra script
rm %{buildroot}%{_bindir}/pip-3*

popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Since removing pip-* also clobbers pip-python3, just remove pip-2*
%{__rm} -rf %{buildroot}%{_bindir}/pip-2*

# Change the name of the pip executable in order to not conflict with perl-pip
# https://bugzilla.redhat.com/show_bug.cgi?id=616399
mv %{buildroot}%{_bindir}/pip %{buildroot}%{_bindir}/python-pip

# after changing the pip-python binary name, make a symlink to the old name,
# that will be removed in a later version
# https://bugzilla.redhat.com/show_bug.cgi?id=855495
pushd %{buildroot}%{_bindir}
ln -s python-pip pip-python
popd


%clean
%{__rm} -rf %{buildroot}

# unfortunately, pip's test suite requires virtualenv >= 1.6 which isn't in
# fedora yet. Once it is, check can be implemented

%files
%defattr(-,root,root,-)
%doc PKG-INFO docs
%attr(755,root,root) %{_bindir}/pip-python
%attr(755,root,root) %{_bindir}/python-pip
%{python_sitelib}/pip*

%if 0%{?with_python3}
%files -n python3-pip
%defattr(-,root,root,-)
%doc PKG-INFO docs
%attr(755,root,root) %{_bindir}/pip-python3
%attr(755,root,root) %{_bindir}/python3-pip
%{python3_sitelib}/pip*
%endif # with_python3

%changelog
* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Tue Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file 
* Mon Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

