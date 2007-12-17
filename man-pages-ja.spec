%define LANG ja
%define snap 20070615

Summary:	Japanese manual pages
Name:		man-pages-%LANG
Version:	%{snap}
Release:	%mkrel 1
License:	distributable
Group:		System/Internationalization
URL:		http://www.linux.or.jp/JM/download.html
Source0:	http://www.linux.or.jp/JM/%{name}-%{snap}.tar.bz2
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

LANG=%LANG DESTDIR=%{buildroot} /usr/sbin/makewhatis %{buildroot}%{_mandir}/%LANG

mkdir -p %{buildroot}/etc/cron.weekly
cat > %{buildroot}/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
/usr/sbin/makewhatis %{_mandir}/%LANG
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
%config(noreplace) /var/cache/man/%LANG/whatis
%{_mandir}/%LANG/man*
%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron
