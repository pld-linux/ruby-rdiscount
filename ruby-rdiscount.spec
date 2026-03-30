#
# Conditional build:
%bcond_without	tests		# build without tests

%define	pkgname	rdiscount
Summary:	Fast Implementation of Gruber's Markdown in C
Name:		ruby-%{pkgname}
Version:	2.2.7.3
Release:	2
License:	BSD
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	5a32c8bf81abceec6d145a5ccf222ed7
URL:		http://github.com/davidfstr/rdiscount
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby-devel
%if %{with tests}
BuildRequires:	ruby-minitest
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fast Implementation of Gruber's Markdown in C.

%package rdoc
Summary:	HTML documentation for %{name}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description rdoc
HTML documentation for %{name}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{name}.

%package ri
Summary:	ri documentation for %{name}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description ri
ri documentation for %{name}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{name}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
cd ext
%{__ruby} extconf.rb
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC"
cd ..

%if %{with tests}
# test/unit compatibility
%{__ruby} -Ilib:ext -e "require 'minitest/autorun'; require './test/rdiscount_test.rb'" || :
%endif

rdoc --ri --op ri lib ext
rdoc --op rdoc lib ext
rm ri/created.rid
rm ri/cache.ri
rm -rf ri/ext

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir},%{ruby_ridir},%{ruby_rdocdir},%{_bindir}}
install -p ext/rdiscount.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
install -p bin/rdiscount $RPM_BUILD_ROOT%{_bindir}
%{__sed} -i -e '1s,/usr/bin/env ruby,%{__ruby},' $RPM_BUILD_ROOT%{_bindir}/rdiscount

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.markdown COPYING
%attr(755,root,root) %{_bindir}/rdiscount
%attr(755,root,root) %{ruby_vendorarchdir}/rdiscount.so
%{ruby_vendorlibdir}/rdiscount.rb
%{ruby_vendorlibdir}/markdown.rb

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/RDiscount
%{ruby_ridir}/Object
