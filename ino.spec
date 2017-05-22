%define oname Ino
%define lname %(echo %oname | tr [:upper:] [:lower:])

Summary:	A command line toolkit for working with Arduino hardware
Name:		%{lname}
Version:	0.3.6
Release:	0
Group:		Development/Other
License:	MIT
URL:		https://inotool.org/
Source0:	https://pypi.python.org/packages/source/i/%{name}/%{name}-%{version}.tar.gz
Buildarch:	noarch

BuildRequires:	pkgconfig(python2)
BuildRequires:	pythonegg(setuptools)

Requires:	python2
Requires:	pythonegg(configobj)
Requires:	pythonegg(pyserial)
Requires:	pythonegg(jinja2)
Requires:	arduino-core
Requires:	picocom


%description
Ino is a command line toolkit for working with Arduino hardware

It allows you to:

  *  Quickly create new projects
  *  Build a firmware from multiple source files and libraries
  *  Upload the firmware to a device
  *  Perform serial communication with a device (aka serial monitor)

Ino may replace Arduino IDE UI if you prefer to work with command line and
an editor of your choice or if you want to integrate Arduino build process
to 3-rd party IDE.

Ino is based on make to perform builds. However Makefiles are generated
automatically and you'll never see them if you don't want to.

%files -f FILELIST
%doc README.rst
%doc MIT-LICENSE.txt

#----------------------------------------------------------------------------

%prep
%setup -q

# Force python2
sed -i -e 's|/usr/bin/env python|/usr/bin/env python2|' ino/runner.py
	
%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --root=%{buildroot} --skip-build --record=FILELIST

# remove *.pyc from FILELIST
sed -i -e '/.pyc/d' FILELIST

# fix perms for runner.py
chmod 0755 %{buildroot}%{python_sitelib}/%{name}/runner.py

# remove .holder
find %{buildroot}%{python_sitelib}/%{name}/ -name .holder -size 0 -delete
sed -i -e '/.holder/d' FILELIST

