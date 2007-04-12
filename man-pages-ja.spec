%define LANG ja

Summary: Japanese manual pages
Name: man-pages-%LANG
Version: 20051015
Release: %mkrel 2
License: distributable
Group: System/Internationalization
Source0: http://www.linux.or.jp/JM/%name-%{version}.tar.bz2
Source2: http://xjman.dsl.gr.jp/xjman-0.6.tar.bz2
Source3: man-pages-ja-install.sh
Icon: books-%LANG.gif
URL: http://www.linux.or.jp/JM/download.html
Buildroot: %_tmppath/%name-root
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LANG, man => 1.5j-8mdk
# for file-system:
Requires(pre): man
Requires(post): man
Autoreqprov: false
BuildArchitectures: noarch
Obsoletes: man-%LANG, manpages-%LANG
Provides: man-%LANG, manpages-%LANG


%description
The japanese man pages.

%prep

%setup -a2
# install X11 man pages
mv xjman-*/ manual
echo "xjman-4.0.3	Y" >> script/pkgs.list

%build
cp %SOURCE3 installman.sh
rm -f manual/*/man1/man.1 manual/*/man1/apropos.1 manual/*/man1/whatis.1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_mandir/%LANG
mkdir -p $RPM_BUILD_ROOT/var/catman/%LANG/cat{1,2,3,4,5,6,7,8,9,n}

make install

rm -fr 

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
/usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG
rm -f $RPM_BUILD_ROOT/usr/share/man/README*


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LANG, if there isn't any man page
   ## directory %_mandir/%LANG
   if [ ! -d %_mandir/%LANG ] ; then
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
rm -fr $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%doc ChangeLog README
%defattr(0644,root,man,755)
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%config(noreplace) /var/cache/man/%LANG/whatis
/%_mandir/%LANG/man*
%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron

