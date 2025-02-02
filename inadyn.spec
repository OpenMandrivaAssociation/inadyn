%define debug_package %{nil}

Summary: A client to update host entries on DynDNS like services
Name:    inadyn
Version: 1.98.0
Release: 6
License: GPL
Group:   System/Configuration/Networking
URL:     https://inadyn.ina-tech.net/
Source0: http://inadyn.ina-tech.net/inadyn.v1.96.2.zip
Source1: inadyn.conf
Source2: inadyn.service
Requires(preun):rpm-helper
Requires(post): rpm-helper

%description
INADYN is a dynamic DNS client. That is, it maintains the IP address of a
host name. It periodically checks whether the IP address stored by the DNS
server is the real current address of the machine that is running INADYN.

%prep
%setup -q -n inadyn

%build
make clean
make

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_mandir}/{man8,man5}

install -m 0755 -p bin/linux/inadyn %{buildroot}%{_sbindir}/
install -m 0644 -p man/inadyn.8 %{buildroot}%{_mandir}/man8/
install -m 0644 -p man/inadyn.conf.5 %{buildroot}%{_mandir}/man5/
install -m 0600 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/
install -m 0755 -p %{SOURCE2} %{buildroot}%{_unitdir}/inadyn.service

%clean

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc readme.html
%{_sbindir}/inadyn
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/inadyn.conf
%{_unitdir}/inadyn*
%defattr(-,root,man)
%{_mandir}/man5/inadyn.conf.*
%{_mandir}/man8/inadyn.*
