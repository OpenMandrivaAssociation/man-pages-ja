%define LNG ja
%define snap 20091215

Summary:	Japanese manual pages
Name:		man-pages-%{LNG}
Version:	%{snap}
Release:	18
License:	distributable
Group:		System/Internationalization
Url:		http://www.linux.or.jp/JM/download.html
Source0:	http://www.linux.or.jp/JM/%{name}-%{snap}.tar.gz
Source2:	http://xjman.dsl.gr.jp/xjman-0.7.tar.bz2
Source3:	man-pages-ja-install.sh
Source4:	manpage-utf8-converter.rb
BuildArch:	noarch
BuildRequires:	man
BuildRequires:	ruby
BuildRequires:	ruby(rubygems)
Requires:	locales-%{LNG}
Requires:	man
# for file-system:
Requires(pre):	man
Requires(post):	man
Autoreqprov:	false
Conflicts:	filesystem < 3.0-17

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
chmod a+x manpage-utf8-converter.rb
./manpage-utf8-converter.rb

%install
mkdir -p %{buildroot}%{_mandir}/%{LNG}
mkdir -p %{buildroot}/var/catman/%{LNG}/cat{1,2,3,4,5,6,7,8,9,n}

make install

LANG=%{LNG} DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}%{_mandir}/%{LNG}

mkdir -p %{buildroot}/etc/cron.weekly
cat > %{buildroot}/etc/cron.weekly/makewhatis-%{LNG}.cron << EOF
#!/bin/bash
%{_bindir}/mandb %{_mandir}/%{LNG}
exit 0
EOF
chmod a+x %{buildroot}/etc/cron.weekly/makewhatis-%{LNG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LNG}
rm -f %{buildroot}/usr/share/man/README*

rm -rf %{buildroot}%{_mandir}/ja/man1/passwd.1*

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%{LNG}, if there isn't any man page
   ## directory %{_mandir}/%{LNG}
   if [ ! -d %{_mandir}/%{LNG} ] ; then
       rm -rf /var/catman/%{LNG}
   fi
fi
# 1 means update
if [ "$1" = "1" ]; then
   # dirty hack to clean previous man-pages-ja installs
   [ -d var/catman/X11/%{LNG} ] && rm -rf /var/catman/X11/%{LNG} >& /dev/null
   [ -d var/catman/X11 ] && rmdir /var/catman/X11 >& /dev/null
fi
:

%files
%doc ChangeLog README
%dir /var/cache/man/%{LNG}
%{_mandir}/%{LNG}/man*
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/index.db*
%attr(755,root,man)/var/catman/%{LNG}
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%{LNG}.cron

