Summary:	Samhain data integrity / intrusion detection system
Name:		samhain
Version:	1.2.6
Release:	0.1
URL:		http://www.la-samhna.de/samhain/index.html
Source0:	http://www.la-samhna.de/samhain/%{name}-%{version}.tar.bz2
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-dontstrip.patch
License:	GPL
Group:		Console/Security
######		Unknown group!
Provides:	%{name}
#BuildRequires:	
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%description
Samhain works by creating a "snapshot" of your system, i.e. a database
of cryptographic checksums of all critical files, and comparing these
files regularly against this database.

%build
%configure2_13 \
	--with-gpg \
	--with-config-file=%{_sysconfdir}/%{name}rc \
	--with-suidcheck
#	--enable-khide

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__make} install-man DESTDIR=$RPM_BUILD_ROOT

gzip README

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(750,root,bin) %{_bindir}/samhain
%config %{_sysconfdir}/samhainrc
#%ghost /var/log/samhain
%{_mandir}/man[58]/*

%clean
rm -rf $RPM_BUILD_ROOT
