Summary:	Samhain data integrity / intrusion detection system
Summary(pl):	Samhain system wykrywania integralno¶ci danych / intruzów
Name:		samhain
Version:	1.2.6
Release:	0.3
URL:		http://www.la-samhna.de/samhain/index.html
Source0:	http://www.la-samhna.de/samhain/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-dontstrip.patch
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Provides:	%{name}
#BuildRequires:	
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/%{name}
%define		_logdir			/var/log/%{name}
%define		_initdir		/etc/rc.d/init.d

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%description
Samhain works by creating a "snapshot" of your system, i.e. a database
of cryptographic checksums of all critical files, and comparing these
files regularly against this database.

%description -l pl
Samhain dzia³a tworz±c "obraz" twojego systemu, np. bazê danych sum 
kontrolnych wszystkich krytycznych plików a nastêpnie regularnie porównuje 
te pliki z baz±.

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

gzip -9nf README

install -d $RPM_BUILD_ROOT{%{_initdir},%{_logdir}}

install %{SOURCE1} $RPM_BUILD_ROOT%{_initdir}/%{name}

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
    /etc/rc.d/init.d/%{name} restart 1>&2
else
    echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} stop 1>&2
    fi
    /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(750,root,bin) %{_bindir}/samhain
%config %{_sysconfdir}/samhainrc
%dir %{_logdir}
%{_mandir}/man[58]/*

%clean
rm -rf $RPM_BUILD_ROOT
