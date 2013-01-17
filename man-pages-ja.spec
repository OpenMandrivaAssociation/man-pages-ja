%define LANG ja
%define snap 20091215

Summary:	Japanese manual pages
Name:		man-pages-%LANG
Version:	%{snap}
Release:	%mkrel 5
License:	distributable
Group:		System/Internationalization
URL:		http://www.linux.or.jp/JM/download.html
Source0:	http://www.linux.or.jp/JM/%{name}-%{snap}.tar.gz
Source2:	http://xjman.dsl.gr.jp/xjman-0.7.tar.bz2
Source3:	man-pages-ja-install.sh
Source4:	manpage-utf8-converter.rb
BuildRequires:	man 	>= 1.6e
BuildRequires:	ruby
Requires:	locales-%LANG
Requires:	man	>= 1.6e
# for file-system:
Requires(pre):	man
Requires(post): man
Autoreqprov:	false
BuildArch:	noarch
Obsoletes:	man-%LANG, manpages-%LANG
Provides:	man-%LANG, manpages-%LANG
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The japanese man pages.

%prep
%setup -qn %{name}-%{snap} -a2

# install X11 man pages
mv xjman/ manual
echo "xjman-4.1.0	Y" >> script/pkgs.list

%build
cp %SOURCE3 installman.sh
rm -f manual/*/man1/man.1 manual/*/man1/apropos.1 manual/*/man1/whatis.1

# convert manpages (euc-jp to utf-8)
# we can use konqueror as a manpage viewer,
# but konqueror doesn't detect euc-jp properly.
cp %SOURCE4 .
./manpage-utf8-converter.rb

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/%LANG
mkdir -p %{buildroot}/var/catman/%LANG/cat{1,2,3,4,5,6,7,8,9,n}

make install

rm -fr 

LANG=%LANG DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}%{_mandir}/%LANG

mkdir -p %{buildroot}/etc/cron.weekly
cat > %{buildroot}/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
%{_bindir}/mandb %{_mandir}/%LANG
exit 0
EOF
chmod a+x %{buildroot}/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  %{buildroot}/var/cache/man/%LANG
rm -f %{buildroot}/usr/share/man/README*


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LANG, if there isn't any man page
   ## directory %{_mandir}/%LANG
   if [ ! -d %{_mandir}/%LANG ] ; then
       rm -rf /var/catman/%LANG
   fi
fi
# 1 means update
if [ "$1" = "1" ]; then
   # dirty hack to clean previous man-pages-ja installs
   [ -d var/catman/X11/%LANG ] && rm -rf /var/catman/X11/%LANG >& /dev/null
   [ -d var/catman/X11 ] && rmdir /var/catman/X11 >& /dev/null
fi
:

%clean
rm -fr %{buildroot}

%files
%defattr(644,root,man,755)
%doc ChangeLog README
%dir %{_mandir}/%LANG
%dir /var/cache/man/%LANG
%{_mandir}/%LANG/man*
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/CACHEDIR.TAG*
%{_mandir}/%{LNG}/index.db*
#%config(noreplace) %{_mandir}/%LANG/whatis
%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron


%changelog
* Tue May 10 2011 Funda Wang <fwang@mandriva.org> 20091215-3mdv2011.0
+ Revision: 673248
- update file list

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild
    - rebuild

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 20091215-1mdv2010.1
+ Revision: 483991
- Update to new version 20091215

* Sun Mar 22 2009 Funda Wang <fwang@mandriva.org> 20090315-1mdv2009.1
+ Revision: 360130
- New version 20090315

* Thu Nov 27 2008 Funda Wang <fwang@mandriva.org> 20081115-1mdv2009.1
+ Revision: 307222
- New version 20081115

* Tue Oct 14 2008 Funda Wang <fwang@mandriva.org> 20080915-1mdv2009.1
+ Revision: 293454
- New version 20080915

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 20080515-2mdv2009.0
+ Revision: 265074
- rebuild early 2009.0 package (before pixel changes)

* Fri May 23 2008 Funda Wang <fwang@mandriva.org> 20080515-1mdv2009.0
+ Revision: 210324
- New snapshot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 20070615-1mdv2008.1
+ Revision: 129709
- kill re-definition of %%buildroot on Pixel's request

* Thu Jul 05 2007 Thierry Vignaud <tv@mandriva.org> 20070615-1mdv2008.0
+ Revision: 48502
- from UTUMI Hirosi <utuhiro78@yahoo.co.jp>:
  o new release
  o change the encoding to utf8 (source4)

* Thu May 31 2007 Funda Wang <fwang@mandriva.org> 20070515-1mdv2008.0
+ Revision: 33021
- fix version

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to the latest version
    - update Source 2
    - remove icon
    - spec file clean


* Wed Oct 19 2005 Thierry Vignaud <tvignaud@mandriva.com> 20051015-2mdk
- drop useless prereq
- ensure %%post does not fail

* Tue Oct 18 2005 Thierry Vignaud <tvignaud@mandriva.com> 20051015-1mdk
- new release

* Fri Aug 19 2005 Thierry Vignaud <tvignaud@mandriva.com> 20050715-1mdk
- new release

* Mon Nov 22 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 20041115-1mdk
- new release

* Mon Jul 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 20040715-2mdk
- fix cron entry

* Tue Jul 20 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 20040715-1mdk
- sanitize versionning
- new release (20040715 snapshot) (UTUMI Hirosi <utuhiro78@yahoo.co.jp>)

* Fri Dec 12 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.6-3mdk
- new release (20031115 snapshot)

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.6-2mdk
- new release (20030525 snapshot)

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.6-1mdk
- new release (20030115 snapshot)

* Mon Nov 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5-10mdk
- new release (20021115 snapshot)

* Thu Oct 17 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5-9mdk
- new release (20021015 snapshot)

* Mon Jun 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5-8mdk
- Four pages were added, and five pages were updated

* Wed May 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5-7mdk
- use new man-pages-LG template
    - don't rebuild whatis on install since
      - we've already build in package
      - cron will rebuild it nightly and so add other package french man pages
    - adapt to new man-pages-LG template
    - requires man => 1.5j-8mdk for new man-pages framework
    - remove old makewhatis.ja since default makewhatis is now able to parse
      non english man pages
    - use new std makewhatis to build whatis in spec and in cron entry 
    - whatis db goes into /var/cache/man (so enable ro /usr)
    - standard {Build,}Requires/buildroot/prereq/arc/provides/obsoletes
    - remove translations

* Tue Apr 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5-6mdk
- 20020415 snapshot

* Wed Mar 20 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5-5mdk
- fix build
- fix makewhatis for non root build
- 20020315 update: 128%% more man-pages (1112 => 2533 man-pages)

* Fri Mar 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5-3mdk
- prevent conflicts with rpm
- fix permission on /usr/share/man/ja/*
- provides manpages-%%LANG
- don't overwrite crontab if user altered it

* Mon Sep 11 2000 Denis Havlik <denis@mandrakesoft.com> 0.5-2mdk
- fixed path in "makewhatis" script

* Wed Aug 30 2000 Denis Havlik <denis@mandrakesoft.com> 0.5-1mdk
- updated to  xjman 0.5 and man	20000815
- move xjman pages to /usr/share/man

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4-8mdk
- BM

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4-7mdk
- use mandir macro in order to be ok when switching to /usr/share/man as
  following FHS.

* Tue Apr 11 2000 Denis Havlik <denis@mandrakesoft.com> 0.4-6mdk
- spechelper, permissions
- Group: System/Internationalization

* Fri Nov 19 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- moved makewhatis.ja from /usr/local/sbin to /usr/sbin

* Thu Oct 21 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- fixed Requires typo
- upgraded man pages

* Tue Jul 20 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- included some nice improvements from man-pages-pl

* Wed Jul 07 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- Adapted the rpm I mantained to Mandrake style

