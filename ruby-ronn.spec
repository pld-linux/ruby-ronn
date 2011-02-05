%bcond_with	gitmaster	# build latest git version, build with n5 builder flag

%if %{with gitmaster}
%define dl_ver	master
%else
%define dl_ver	%{version}
%endif

%define pkgname ronn

%define		rel	0.1

Summary:	Markdown to man and HTML translator
Name:		ruby-ronn
Version:	0.7.3
Release:	%{?with_gitmaster:master.}%{rel}
License:	MIT
Source0:	http://github.com/rtomayko/ronn/tarball/%{dl_ver}/%{name}-%{dl_ver}.tar.gz
# Source0-md5:	6fce1de64c54b014b88270567c29b5ce
Group:		Development/Languages
URL:		http://github.com/rtomayko/ronn
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-modules
BuildRequires:	setup.rb
Requires:	ruby-hpricot
Requires:	ruby-mustache
Requires:	ruby-rdiscount
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby library for ronn.

%package -n ronn
Summary:	Markdown to man and HTML translator
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description -n ronn
Ronn builds manuals. It converts simple, human readable textfiles to
roff for terminal display, and also to HTML for the web.

The source format includes all of Markdown but has a more rigid
structure and syntax extensions for features commonly found in
manpages (definition lists, link notation, etc.). The ronn-format(7)
manual page defines the format in detail.

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
mv rtomayko-ronn-*/* .
rm -rf rtomayko-ronn-*

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

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man{1,7}
mv $RPM_BUILD_ROOT%{_mandir}/{,man1/}%{pkgname}.1
mv $RPM_BUILD_ROOT%{_mandir}/{,man7/}%{pkgname}-format.7

# Remove HTML and source markdown files
rm $RPM_BUILD_ROOT%{_mandir}/*.*.*
rm $RPM_BUILD_ROOT%{_mandir}/index*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README.md
%{ruby_rubylibdir}/%{pkgname}.rb
%{ruby_rubylibdir}/%{pkgname}

%files -n ronn
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{pkgname}
%{_mandir}/man1/%{pkgname}.1*
%{_mandir}/man7/%{pkgname}-format.7*

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Ronn
