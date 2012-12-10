%define _initddir /etc/rc.d/init.d

Summary: A client to update host entries on DynDNS like services
Name: inadyn
Version: 1.98.0
Release: %mkrel 1
License: GPL
Group: System/Configuration/Networking
URL: http://inadyn.ina-tech.net/
Source0: http://inadyn.ina-tech.net/inadyn.v1.96.2.zip
Source1: inadyn.conf
Source2: inadyn.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{_mandir}/{man8,man5}

install -m 0755 -p bin/linux/inadyn %{buildroot}%{_sbindir}/
install -m 0644 -p man/inadyn.8 %{buildroot}%{_mandir}/man8/
install -m 0644 -p man/inadyn.conf.5 %{buildroot}%{_mandir}/man5/
install -m 0600 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/
install -m 0755 -p %{SOURCE2} %{buildroot}%{_initddir}/inadyn

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
%{_mandir}/man5/inadyn.conf.*
%{_mandir}/man8/inadyn.*




%changelog
* Wed Mar 16 2011 Stéphane Téletchéa <steletch@mandriva.org> 1.98.0-1mdv2011.0
+ Revision: 645247
- update to new version 1.98.0

* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.96.2-5mdv2011.0
+ Revision: 619626
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.96.2-4mdv2010.0
+ Revision: 429509
- rebuild

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.96.2-3mdv2009.0
+ Revision: 239032
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix man pages

* Fri May 25 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.96.2-2mdv2008.0
+ Revision: 30932
- minor spec cleanup (build/install)

* Thu May 24 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.96.2-1mdv2008.0
+ Revision: 30804
- fix/improve initscript
- disable service by default upon installation
  (without proper config, the service is useless and noisy)
- Import inadyn

