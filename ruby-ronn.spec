# TODO: project is continued as ronn-ng, https://github.com/apjanke/ronn-ng
#
# Conditional build:
%bcond_without	tests		# build without tests

%define pkgname ronn
Summary:	Markdown to man and HTML translator
Summary(pl.UTF-8):	Konwerter języka Markdown do podręcznika man i HTML-a
Name:		ruby-%{pkgname}
Version:	0.7.3
Release:	3
License:	MIT
#Source0Download: https://github.com/rtomayko/ronn/releases
Source0:	https://github.com/rtomayko/ronn/archive/%{version}/ronn-%{version}.tar.gz
# Source0-md5:	90cdedb42920c8c2a74e2d177e9535b6
Group:		Development/Languages
URL:		https://github.com/rtomayko/ronn
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
%if %{with tests}
BuildRequires:	ruby-hpricot
BuildRequires:	ruby-rdiscount
%endif
Requires:	ruby-hpricot
Requires:	ruby-mustache
Requires:	ruby-rdiscount
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby library for ronn (Markdown to man and HTML translator).

%description -l pl.UTF-8
Biblioteka języka Ruby dla programu ronn (konwertera języka Markdown
do podręcznika man i HTML-a).

%package -n ronn
Summary:	Markdown to man and HTML translator
Summary(pl.UTF-8):	Konwerter języka Markdown do podręcznika man i HTML-a
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}
Requires:	groff

%description -n ronn
Ronn builds manuals. It converts simple, human readable textfiles to
roff for terminal display, and also to HTML for the web.

The source format includes all of Markdown but has a more rigid
structure and syntax extensions for features commonly found in
manpages (definition lists, link notation, etc.). The ronn-format(7)
manual page defines the format in detail.

%description -n ronn -l pl.UTF-8
Ronn buduje podręczniki. Konwertuje proste, czytelne dla człowieka
pliki tekstowe do formatu roff (do wyświetlania na terminalu) oraz
HTML-a (dla WWW).

Format źródłowy obejmuje całość języka Markdown, ale ma nieco
ściślejszą strukturę oraz rozszerzenia składni pod kątem możliwości
stron podręcznika (listy definicji, notacja odnośników itp.). Strona
podręcznika ronn-format(7) szczegółowo określa format.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla pakietu %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla pakietu %{pkgname}.

%prep
%setup -q -n ronn-%{version}

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

# do trivial version check
%if %{with tests}
%{__ruby} -Ilib ./bin/ronn --version
%endif

rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} -r ri/lib/ronn/template
%{__rm} ri/created.rid
%{__rm} ri/cache.ri

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{1,7},%{ruby_vendorlibdir},%{ruby_specdir},%{ruby_ridir},%{ruby_rdocdir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/*.7 $RPM_BUILD_ROOT%{_mandir}/man7
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README.md
%{ruby_vendorlibdir}/ronn.rb
%{ruby_vendorlibdir}/ronn
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%files -n ronn
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ronn
%{_mandir}/man1/ronn.1*
%{_mandir}/man7/ronn-format.7*

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Ronn
