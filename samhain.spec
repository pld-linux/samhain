Summary:	Samhain data integrity / intrusion detection system
Name:		samhain
Version:	1.2.2
Release:	0.1
URL:		http://www.la-samhna.de/samhain/index.html
Source0:	http://www.la-samhna.de/samhain/%{name}-%{version}.tar.bz2
License:	GPL
Group:		Console/Security
Provides:	%{name}
#BuildRequires:	
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}

%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1

%description
Samhain works by creating a "snapshot" of your system, i.e. a database of
cryptographic checksums of all critical files, and comparing these files
regularly against this database.

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
#%{__install}

%files
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/
#%{_mandir}/man[15]/*
#%config(noreplace) %{_sysconfdir}/
#%doc

%clean
#rm -rf $RPM_BUILD_ROOT
