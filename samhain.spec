Summary:	Samhain data integrity / intrusion detection system
Summary(pl):	Samhain system wykrywania integralno¶ci danych / intruzów
Name:		samhain
Version:	1.4.0
Release:	1
License:	GPL
Group:		Applications/System
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}rc
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-dontstrip.patch
URL:		http://www.la-samhna.de/samhain/index.html
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
kontrolnych wszystkich krytycznych plików a nastêpnie regularnie
porównuje te pliki z baz±.

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
	$RPM_BUILD_ROOT%{_var}/lib/%{name} \
	$RPM_BUILD_ROOT%{_localstatedir}/log \

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}

touch $RPM_BUILD_ROOT%{_localstatedir}/log/samhain_log

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
    /etc/rc.d/init.d/%{name} restart 1>&2
else
    echo "Run \"%{_sbindir}/samhain -t init\" to initialize database"
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
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samhainrc
%attr(700,root,root) %dir %{_var}/lib/%{name}
%attr(754,root,root)  /etc/rc.d/init.d/%{name}
%attr(0640,root,root) %ghost %{_localstatedir}/log/samhain_log
%{_mandir}/man[58]/*

%clean
rm -rf $RPM_BUILD_ROOT
