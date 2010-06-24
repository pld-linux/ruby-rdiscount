# TODO
# - rake doc
#   (in /home/users/z/rpm/BUILD/ruby-discount-1.2.7) hanna --charset utf8 --fmt html --inline-source --line-numbers --main RDiscount --op doc --title 'RDiscount API Documentation' lib/rdiscount.rb lib/markdown.rb sh: hanna: not found
#   rake aborted!
#
%define pkgname rdiscount
Summary:	Discount Markdown Processor for Ruby
Name:		ruby-rdiscount
Version:	1.2.7
Release:	0.1
License:	BSD-style
#Source0:	http://rubyforge.org/frs/download.php/18699/%{pkgname}-%{version}.tgz
Source0:	http://github.com/rtomayko/rdiscount/tarball/v1.2.7/%{name}-%{version}.tar.gz
# Source0-md5:	85edbb9768bfa7e36455dbf8749dccae
Patch0:		%{name}-ruby1.9.patch
Group:		Development/Languages
URL:		http://github.com/rtomayko/rdiscount
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.9
BuildRequires:	ruby-modules
BuildRequires:	setup.rb
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Discount Markdown Processor for Ruby.

%package -n rdiscount
Summary:	Markdown processor
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description -nrdiscount
Markdown processor.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -c
mv rtomayko-rdiscount-*/* .
rm -rf rtomayko-rdiscount-*

%patch0 -p1

%build

cp %{_datadir}/setup.rb .

ruby setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

ruby setup.rb setup

rdoc --ri --op ri lib
rdoc --op rdoc lib
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

#cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

ruby setup.rb install \
    --prefix=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.markdown
%{ruby_rubylibdir}/%{pkgname}.rb
%{ruby_rubylibdir}/markdown.rb
%attr(755,root,root) %{ruby_archdir}/%{pkgname}.so

%files -n rdiscount
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rdiscount

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/RDiscount
