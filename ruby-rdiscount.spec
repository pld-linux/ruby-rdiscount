#
# Conditional build:
%bcond_without	tests	# build without tests
%bcond_without	doc	# don't build ri/rdoc

# TODO
# - system libmarkdown (from discount.spec) >= 2.2.0
# - rake doc
#   (in /home/users/z/rpm/BUILD/ruby-discount-1.2.7) hanna --charset utf8 --fmt html --inline-source --line-numbers --main RDiscount --op doc --title 'RDiscount API Documentation' lib/rdiscount.rb lib/markdown.rb sh: hanna: not found
#   rake aborted!

%define pkgname rdiscount
Summary:	Discount Markdown Processor for Ruby
Summary(pl.UTF-8):	Discount (procesor języka Markdown) dla języka Ruby
Name:		ruby-%{pkgname}
Version:	2.2.0.1
Release:	4
License:	BSD
Source0:	https://github.com/davidfstr/rdiscount/archive/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	11b5061786a57da45052e8d02ef77c5a
Group:		Development/Languages
URL:		https://github.com/davidfstr/rdiscount
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby >= 1:1.9
BuildRequires:	ruby-devel
BuildRequires:	ruby-modules
BuildRequires:	setup.rb >= 3.4.1-6
%if %{with tests}
BuildRequires:	ruby-test-unit
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Discount is a Markdown language Processor. This package contains
Discount for Ruby.

%description -l pl.UTF-8
Discount to procesor języka znaczników Markdown. Ten pakiet zawiera
procesor Discount dla języka Ruby.

%package -n rdiscount
Summary:	Markdown processor
Summary(pl.UTF-8):	Procesor języka znaczników Markdown
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description -n rdiscount
Markdown processor.

%description -n rdiscount -l pl.UTF-8
Procesor języka znaczników Markdown.

%package rdoc
Summary:	HTML documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu %{pkgname} języka Ruby
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4
BuildArch:	noarch

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu %{pkgname} języka Ruby.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu %{pkgname} języka Ruby
Group:		Documentation
Requires:	ruby
BuildArch:	noarch

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla modułu %{pkgname} języka Ruby.

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

%if %{with tests}
%{__ruby} -r rubygems -Ilib:ext:. \
	-e 'gem "test-unit"; Dir.glob("test/*_test.rb").sort.each {|f| require f}'
%endif

%if %{with doc}
rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} -r ri/Object
%{__rm} ri/created.rid
%{__rm} ri/cache.ri
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_specdir},%{ruby_ridir},%{ruby_rdocdir}}

%{__ruby} setup.rb install \
	--prefix=$RPM_BUILD_ROOT

cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

# just does require rdiscount
%{__rm} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/markdown.rb
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/markdown.7

%if %{with doc}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/rdiscount.1.ronn
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md COPYING README.markdown
%{ruby_vendorlibdir}/rdiscount.rb
%attr(755,root,root) %{ruby_vendorarchdir}/rdiscount.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%files -n rdiscount
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rdiscount
%{_mandir}/man1/rdiscount.1*

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/RDiscount
%endif
