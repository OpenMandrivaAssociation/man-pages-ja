#!/bin/sh

prefix=$RPM_BUILD_ROOT
owner=root
group=root
#lang=ja_JP.eucJP
lang=ja
compress="gzip"

mandir=$RPM_BUILD_ROOT/usr/share/man/$lang

mkdir -p $mandir/man{1,2,3,4,5,6,7,8}

packages=`cat script/pkgs.list \
        | perl -e 'while(<STDIN>){if (/^([^#\s]+\s)\s*Y/){unshift(@s,$1)}} print @s'`

for pkg in $packages; do
    for i in 1 2 3 4 5 6 7 8; do
	if [ -d manual/$pkg/man$i ]; then
	    cp -a manual/$pkg/man$i/* $mandir/man$i/
	fi
    done
done

# special file
if [ -f manual/GNU_sh-utils/man1/su.1 ]; then
    cp -a manual/GNU_sh-utils/man1/su.1 $mandir/man1/
fi

if [ x$compress != x ]; then
    find $mandir -type f -size +2b -print | xargs $compress
fi
