# TODO
# - rake doc
#   (in /home/users/z/rpm/BUILD/ruby-discount-1.2.7) hanna --charset utf8 --fmt html --inline-source --line-numbers --main RDiscount --op doc --title 'RDiscount API Documentation' lib/rdiscount.rb lib/markdown.rb sh: hanna: not found
#   rake aborted!
#
%define pkgname rdiscount
Summary:	Discount Markdown Processor for Ruby
Name:		ruby-%{pkgname}
Version:	2.1.8
Release:	1
License:	BSD
Source0:	https://github.com/davidfstr/rdiscount/archive/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	7c8076339ffcbc0be7a76ebd19750fb7
Group:		Development/Languages
URL:		https://github.com/davidfstr/rdiscount
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby >= 1:1.9
BuildRequires:	ruby-devel
BuildRequires:	ruby-modules
BuildRequires:	setup.rb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Discount Markdown Processor for Ruby.

%package -n rdiscount
Summary:	Markdown processor
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description -n rdiscount
Markdown processor.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -qn %{pkgname}-%{version}

%build
# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

cp %{_datadir}/setup.rb .

%{__ruby} setup.rb config \
	--rbdir=%{ruby_vendorlibdir} \
	--mandir=%{_mandir}/man1 \
	--sodir=%{ruby_vendorarchdir}

%{__ruby} setup.rb setup

rdoc --ri --op ri lib
rdoc --op rdoc lib
rm -r ri/Object
rm ri/created.rid
rm ri/cache.ri

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_specdir},%{ruby_ridir},%{ruby_rdocdir}}
%{__ruby} setup.rb install \
    --prefix=$RPM_BUILD_ROOT
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

# just does require rdiscount
%{__rm} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/markdown.rb

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man*/*.ronn*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man*/markdown.7*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.markdown
%{ruby_vendorlibdir}/rdiscount.rb
%attr(755,root,root) %{ruby_vendorarchdir}/rdiscount.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%files -n rdiscount
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rdiscount
%{_mandir}/man1/rdiscount.1*

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/RDiscount
