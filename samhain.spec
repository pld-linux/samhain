%bcond_with	prelude		# enables samhain working as a prelude sensor

Summary:	Samhain data integrity / intrusion detection system
Summary(pl):	System kontroli integralno�ci danych i wykrywania intruz�w Samhain
Name:		samhain
Version:	2.2.6
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.la-samhna.de/archive/%{name}_signed-%{version}.tar.gz
# Source0-md5:	454aec59fce0a913f58b7ab2e2371280
Source1:	%{name}.init
Source2:	%{name}rc
Patch0:		%{name}-configure.patch
URL:		http://www.la-samhna.de/samhain/
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	automake
%{!?with_prelude:BuildRequires:	libprelude-devel >= 0.9.6}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Samhain works by creating a "snapshot" of your system, i.e. a database
of cryptographic checksums of all critical files, and comparing these
files regularly against this database.

%description -l pl
Samhain dzia�a tworz�c "obraz" twojego systemu, tj. baz� danych sum
kontrolnych wszystkich krytycznych plik�w, a nast�pnie regularnie
por�wnuje te pliki z baz�.

%prep
%setup -qc
tar xzf %{name}-%{version}.tar.gz -C ..
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub .
%configure \
	--enable-login-watch \
	--enable-mounts-check \
	--enable-ptrace \
	--enable-suidcheck \
	--with%{!?with_prelude:out}-prelude \

%{__make}

# sstrip breaks ELFs
echo ':' > sstrip

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_var}/lib/%{name} \
	$RPM_BUILD_ROOT%{_localstatedir}/log

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} install-man \
	DESTDIR=$RPM_BUILD_ROOT

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
%banner -e %{name} <<EOF
%if %{with samhain}
Register samhain sensor before first run:
prelude-adduser register <profile> "imdef:w" <manager host> --uid 0 --gid 0
and then
%endif
Run %{_sbindir}/samhain -t init\ to initialize database 
%if %{without samhain}
if not initialized.
%endif
EOF
fi
%service samhain restart "Samhain"

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/samhainrc
%attr(700,root,root) %dir %{_var}/lib/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %ghost %{_localstatedir}/log/samhain_log
%{_mandir}/man[58]/*
