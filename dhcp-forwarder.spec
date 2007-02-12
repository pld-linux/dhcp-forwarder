# TODO: nobody cannot own any files
Summary:	DHCP relay agent
Summary(pl.UTF-8):	Serwer pośredniczący dla żądań DHCP
Name:		dhcp-forwarder
Version:	0.7
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.tu-chemnitz.de/~ensc/dhcp-fwd/files/%{name}-%{version}.tar.bz2
# Source0-md5:	e7f876e615ebc3f96418f6477b4451e2
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Source3:	%{name}.config
URL:		http://www.tu-chemnitz.de/~ensc/dhcp-fwd/
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dhcp-forwarder is a DHCP relay agent which forwards DHCP messages
between subnets with different sublayer broadcast domains. It runs as
non-root in a chroot-jail.

%description -l pl.UTF-8
dhcp-forwarder jest serwerem pośredniczącym DHCP który przekazuje
komunikaty DHCP pomiędzy podsieciami w różnych domenach
rozgłoszeniowych. Działa ze zwykłego użytkownika (nie-roota) wewnątrz
chrootowanego środowiska.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},/var/lib/dhcp-fwd}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/dhcp-forwarder
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp-forwarder
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/dhcp-fwd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dhcp-forwarder
if [ -f /var/lock/subsys/dhcp-forwarder ]; then
	/etc/rc.d/init.d/dhcp-forwarder restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/dhcp-forwarder start\" to start DHCP forwarder." 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/dhcp-forwarder ]; then
		/etc/rc.d/init.d/dhcp-forwarder stop 1>&2
	fi
	/sbin/chkconfig --del dhcp-forwarder
fi

%files
%defattr(644,root,root,755)
%doc README NEWS AUTHORS
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcp-fwd.conf
%attr(754,root,root) /etc/rc.d/init.d/dhcp-forwarder
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp-forwarder
# XXX: fix ownership
%dir %attr(750,nobody,root) /var/lib/dhcp-fwd # FIXME nobody user/group can't own files! -adapter.awk
