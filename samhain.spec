Summary:	Samhain data integrity / intrusion detection system
Summary(pl):	Samhain system wykrywania integralno¶ci danych / intruzów
Name:		samhain
Version:	1.3.5
Release:	0.1
URL:		http://www.la-samhna.de/samhain/index.html
Source0:	http://www.la-samhna.de/samhain/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-dontstrip.patch
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Prereq:		chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
	--with-suidcheck 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__make} install-man DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/%{_var}/lib/%{name}

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
%attr(750,root,bin) %{_sbindir}/samhain
%config %{_sysconfdir}/samhainrc
#%dir %{_logdir}
%attr(700,root,root) %dir %{_var}/lib/%{name}
%attr(754,root,root)  /etc/rc.d/init.d/%{name}
%{_mandir}/man[58]/*

%clean
rm -rf $RPM_BUILD_ROOT
