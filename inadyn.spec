%define _initddir /etc/rc.d/init.d

Summary: A client to update host entries on DynDNS like services
Name: inadyn
Version: 1.96.2
Release: %mkrel 1
License: GPL
Group: System/Configuration/Networking
URL: http://inadyn.ina-tech.net/
Source0: http://inadyn.ina-tech.net/inadyn.v1.96.2.zip
Source1: inadyn.conf
Source2: inadyn.init
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description
INADYN is a dynamic DNS client. That is, it maintains the IP address of a
host name. It periodically checks whether the IP address stored by the DNS
server is the real current address of the machine that is running INADYN.

%prep
%setup -q -n inadyn
cp %{SOURCE1} .
cp %{SOURCE2} .

%build
make clean
make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{_mandir}/{man8,man5}

install -m 0755 -p bin/linux/inadyn %{buildroot}%{_sbindir}/
install -m 0644 -p man/inadyn.8 %{buildroot}%{_mandir}/man8/
install -m 0644 -p man/inadyn.conf.5 %{buildroot}%{_mandir}/man5/
install -m 0600 -p inadyn.conf %{buildroot}%{_sysconfdir}/
install -m 0755 -p inadyn.init %{buildroot}%{_initddir}/inadyn

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add inadyn
/sbin/chkconfig inadyn off

%preun
if [ $1 = 0 ]; then
        /sbin/service inadyn stop > /dev/null 2>&1
        /sbin/chkconfig --del inadyn
fi

%files
%defattr(-,root,root)
%doc readme.html
%{_sbindir}/inadyn
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/inadyn.conf
%{_initddir}/inadyn
%defattr(-,root,man)
%{_mandir}/man5/inadyn.conf.5.bz2
%{_mandir}/man8/inadyn.8.bz2


