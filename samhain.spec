Summary:	Samhain data integrity / intrusion detection system
Summary(pl):	System kontroli integralno¶ci danych i wykrywania intruzów Samhain
Name:		samhain
Version:	2.0.4
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://la-samhna.de/samhain/%{name}_signed-%{version}.tar.gz
# Source0-md5:	da901289c4f61c3d823ab89ffcc3782e
Source1:	%{name}.init
Source2:	%{name}rc
#Patch0:		%{name}-DESTDIR.patch
Patch0:		%{name}-configure.patch
URL:		http://www.la-samhna.de/samhain/
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't strip by system strip
%define		no_install_post_strip	1
#%%define 	_use_internal_dependency_generator 0

%description
Samhain works by creating a "snapshot" of your system, i.e. a database
of cryptographic checksums of all critical files, and comparing these
files regularly against this database.

%description -l pl
Samhain dzia³a tworz±c "obraz" twojego systemu, tj. bazê danych sum
kontrolnych wszystkich krytycznych plików, a nastêpnie regularnie
porównuje te pliki z baz±.

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
	--enable-suidcheck

%{__make} \
	CC="%{__cc}"

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
+%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/samhainrc
%attr(700,root,root) %dir %{_var}/lib/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %ghost %{_localstatedir}/log/samhain_log
%{_mandir}/man[58]/*
