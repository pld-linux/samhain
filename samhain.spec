Summary:	Samhain data integrity / intrusion detection system
Summary(pl):	System kontroli integralno�ci danych i wykrywania intruz�w Samhain
Name:		samhain
Version:	1.5.4
Release:	1
License:	GPL
Group:		Applications/System
# extracted from http://www.la-samhna.de/samhain/samhain-current.tar.gz
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}rc
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.la-samhna.de/samhain/
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't strip by system strip
%define		no_install_post_strip	1

%description
Samhain works by creating a "snapshot" of your system, i.e. a database
of cryptographic checksums of all critical files, and comparing these
files regularly against this database.

%description -l pl
Samhain dzia�a tworz�c "obraz" twojego systemu, tj. baz� danych sum
kontrolnych wszystkich krytycznych plik�w a nast�pnie regularnie
por�wnuje te pliki z baz�.

%prep
%setup -q
%patch0 -p1

%build
# stupid... it uses own PARSE_ARG and doesn't recognize some standard options
./configure \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags}" \
	CPPFLAGS="" \
	CC=%{__cc} \
	--build=%{_target_platform} \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=%{_localstatedir} \
	--mandir=%{_mandir} \
	--with-suidcheck

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_var}/lib/%{name} \
	$RPM_BUILD_ROOT%{_localstatedir}/log \

%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__make} install-man DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}

touch $RPM_BUILD_ROOT%{_localstatedir}/log/samhain_log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"%{_sbindir}/samhain -t init\" to initialize database if not initialized."
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
%doc README
%attr(750,root,bin) %{_sbindir}/samhain
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samhainrc
%attr(700,root,root) %dir %{_var}/lib/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %ghost %{_localstatedir}/log/samhain_log
%{_mandir}/man[58]/*
