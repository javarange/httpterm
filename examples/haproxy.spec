Summary: HA-Proxy is a TCP/HTTP reverse proxy for high availability environments
Name: haproxy
Version: 1.2.12
Release: 1
License: GPL
Group: System Environment/Daemons
URL: http://w.ods.org/tools/%{name}/
Source0: http://w.ods.org/tools/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pcre-devel
Requires: /sbin/chkconfig, /sbin/service

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
- route HTTP requests depending on statically assigned cookies
- spread the load among several servers while assuring server persistence
  through the use of HTTP cookies
- switch to backup servers in the event a main one fails
- accept connections to special ports dedicated to service monitoring
- stop accepting connections without breaking existing ones
- add/modify/delete HTTP headers both ways
- block requests matching a particular pattern

It needs very little resource. Its event-driven architecture allows it to easily
handle thousands of simultaneous connections on hundreds of instances without
risking the system's stability.

%prep
%setup -q

%build
%{__make} REGEX="pcre" "COPTS.pcre=-DUSE_PCRE $(pcre-config --cflags)" DEBUG="" TARGET=linux24e
#%{__make} REGEX=pcre DEBUG="" LIBS.pcre="-L\$(PCREDIR)/lib -Wl,-Bstatic -lpcreposix -lpcre -Wl,-Bdynamic"


%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}

%{__install} -s %{name} %{buildroot}%{_sbindir}/
%{__install} -c -m 644 examples/%{name}.cfg %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -c -m 755 examples/%{name}.init %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
 
%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  /sbin/service %{name} stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%doc CHANGELOG TODO examples doc/haproxy-en.txt doc/haproxy-fr.txt doc/architecture.txt
%attr(0755,root,root) %{_sbindir}/%{name}
%dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.cfg
%attr(0755,root,root) %config %{_sysconfdir}/rc.d/init.d/%{name}

%changelog
* Wed Apr 15 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.12

* Wed Mar 30 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.11.1

* Wed Mar 19 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.10

* Wed Mar 15 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.9

* Sat Jan 22 2005 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.3 (1.1.30)

* Sun Nov 14 2004 Willy Tarreau <w@w.ods.org>
- updated to 1.1.29
- fixed path to config and init files
- statically linked PCRE to increase portability to non-pcre systems

* Sun Jun  6 2004 Willy Tarreau <willy@w.ods.org>
- updated to 1.1.28
- added config check support to the init script

* Tue Oct 28 2003 Simon Matter <simon.matter@invoca.ch>
- updated to 1.1.27
- added pid support to the init script

* Wed Oct 22 2003 Simon Matter <simon.matter@invoca.ch>
- updated to 1.1.26

* Thu Oct 16 2003 Simon Matter <simon.matter@invoca.ch>
- initial build
