Summary:	DHCP relay agent
Summary(pl):	Serwer po¶rednicz±cy dla ¿±dañ DHCP
Name:		dhcp-forwarder
Version:	0.6
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.tu-chemnitz.de/~ensc/dhcp-fwd/files/%{name}-%{version}.tar.bz2
# Source0-md5:	cbe60c8c904394a8e38e12ac42c02284
Source1:	%{name}.sysconfig
# Source1-md5:	f323198e6a600abf59ca5fc995b61119
Source2:	%{name}.init
# Source2-md5:	029fe3cd27f666b4b1c4e3c2c117994f
Source3:	%{name}.config
# Source3-md5:	e22d2909206beb10e09e71d32e6d90eb
URL:		http://www.tu-chemnitz.de/~ensc/dhcp-fwd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dhcp-forwarder is a DHCP relay agent which forwards DHCP messages between
subnets with different sublayer broadcast domains. It runs as non-root in
a chroot-jail.

%description -l pl
dhcp-forwarder jest serwerem po¶rednicz±cym DHCP który przekazuje
komunikaty DHCP pomiêdzy podsieciami w ró¿nych domenach rozg³oszeniowych.
Dzia³a ze zwyk³ego u¿ytkownika (nie-roota) wewn±trz chrootowanego
¶rodowiska.

%prep
%setup -q

%build
#%{__aclocal}
#%{__autoconf}
#%{__autoheader}
#%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig},var/lib/dhcp-fwd}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/dhcp-forwarder
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp-forwarder
install %{SOURCE3} $RPM_BUILD_ROOT/etc/dhcp-fwd.conf

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
%config(noreplace) %verify(not size mtime md5) /etc/dhcp-fwd.conf
%attr(755,root,root) /etc/rc.d/init.d/dhcp-forwarder
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/dhcp-forwarder
%dir %attr(750,nobody,root) /var/lib/dhcp-fwd
