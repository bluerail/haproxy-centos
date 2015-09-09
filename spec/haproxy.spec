%define haproxy_user    haproxy
%define haproxy_uid     188
%define haproxy_group   haproxy
%define haproxy_gid     188
%define haproxy_home    %{_localstatedir}/lib/haproxy
%define haproxy_confdir %{_sysconfdir}/haproxy
%define haproxy_datadir %{_datadir}/haproxy

%define version 1.5.14
%define release 1


Name: haproxy
Summary: HA-Proxy is a TCP/HTTP reverse proxy for high availability environments
Version: %{version}
Release: %{release}%{?dist}
License: GPLv2+
URL: http://www.haproxy.org/
Group: System Environment/Daemons

Source0: http://www.haproxy.org/download/1.5/src/haproxy-%{version}.tar.gz
Source1: haproxy.init
Source2: haproxy.cfg
Source3: haproxy.logrotate

Requires(pre): %{_sbindir}/groupadd
Requires(pre): %{_sbindir}/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pcre-devel openssl-devel zlib-devel
BuildRequires: setup >= 2.5
Requires: pcre openssl zlib

%description
HAProxy is a free, fast and reliable solution offering high
availability, load balancing, and proxying for TCP and HTTP-based
applications. It is particularly suited for web sites crawling under
very high loads while needing persistence or Layer7 processing.
Supporting tens of thousands of connections is clearly realistic with
modern hardware. Its mode of operation makes integration with existing
architectures very easy and riskless, while still offering the
possibility not to expose fragile web servers to the net.

%prep
%setup -q -n %{name}-%{version}

%build
%ifarch %ix86 x86_64
use_regparm="USE_REGPARM=1"
%endif

make %{?_smp_mflags} CPU="generic" TARGET="linux26" USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 ${use_regparm}

pushd contrib/halog
make halog
popd

%install
rm -rf %{buildroot}
make install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
make install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{haproxy_confdir}/%{name}.cfg
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -d -m 0755 %{buildroot}%{haproxy_home}
%{__install} -d -m 0755 %{buildroot}%{haproxy_datadir}
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 ./contrib/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -p -m 0644 ./examples/errorfiles/* %{buildroot}%{haproxy_datadir}

for file in $(find . -type f -name '*.txt') ; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/groupadd -g %{haproxy_gid} -r %{haproxy_group} 2>/dev/null || :
%{_sbindir}/useradd -u %{haproxy_uid} -g %{haproxy_group} -d %{haproxy_home} -s /sbin/nologin -r %{haproxy_user} 2>/dev/null || :

%post
/sbin/chkconfig --add haproxy

%preun
if [ "$1" -eq 0 ]; then
    /sbin/service haproxy stop >/dev/null 2>&1
    /sbin/chkconfig --del haproxy
fi

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service haproxy condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README doc/*
%doc examples/url-switching.cfg
%doc examples/acl-content-sw.cfg
%doc examples/content-sw-sample.cfg
%doc examples/cttproxy-src.cfg
%doc examples/haproxy.cfg
%doc examples/tarpit.cfg
%{haproxy_datadir}
%dir %{haproxy_confdir}
%config(noreplace) %{haproxy_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz
%attr(-,%{haproxy_user},%{haproxy_group}) %dir %{haproxy_home}
%exclude %{_sbindir}/haproxy-systemd-wrapper

%changelog

* Wed Sep 09 2015 Dick Davies <dick@hellooperator.net> - 1.5.14
- Update to 1.5.14  (fix for CVE-2015-3281)

* Wed Aug 20 2014 Alan Ivey <alanivey@gmail.com> - 1.5.3
- Update to haproxy 1.5.3
- Add %{dist} to Release

* Fri Jun 20 2014 Joseph Daigle <joseph@cridion.com> - 1.5.0
- Update to haproxy 1.5.0

* Mon May 12 2014 Jeff Palmer <jeff@palmerit.net> - 1.5dev25
- Update to haproxy 1.5-dev25

* Tue Feb 04 2014 Chris Schuld <chris@chrisschuld.com> - 1.5dev22
- Update to haproxy 1.5-dev22

* Thu Aug 29 2013 Martijn Storck <martijn@bluerail.nl> - 1.5dev19.2
- Compile with OpenSSL support

* Wed Aug 28 2013 Martijn Storck <martijn@bluerail.nl> - 1.5dev19.1
- Update to haproxy 1.5-dev19

* Tue Oct 02 2012 Ryan O'Hara <rohara@redhat.com> - 1.4.22-3
- Use static uid/gid.
  Resolves: rhbz#846067

* Fri Sep 21 2012 Ryan O'Hara <rohara@redhat.com> - 1.4.22-2
- Bump release number.
  Resolves: rhbz#846067

* Thu Sep 20 2012 Ryan O'Hara <rohara@redhat.com> - 1.4.22-1
- Initial build.
  Resolves: rhbz#846067
