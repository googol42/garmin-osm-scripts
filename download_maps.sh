#!/bin/sh

function log {
    echo -e "`date +%d.%m.%Y\ %H:%M`: downloaded $1 (`sha256sum ./output/$1.img | cut -d " " -f 1`)\n$(cat updates)" > updates ;
}

mkdir -p tmp
rm -f ./tmp/*

(
    wget -P ./tmp/ http://osm.thkukuk.de/TK-DACH-Wanderwege.7z;
    echo "Downloaded 'Wanderwege'";
    7z e -aoa ./tmp/TK-DACH-Wanderwege.7z -otmp/;
    mv ./tmp/TK-DACH-Wanderwege.img ./output/;
    echo "Done with 'Wanderwege'";
    log TK-DACH-Wanderwege;
) &
(
    wget -P ./tmp/ http://gps.maroufi.net/download/badwuert-rad.img;
    echo "Downloaded 'badwuert-rad'";
    cp ./tmp/badwuert-rad.img ./output/;
    echo "Done with 'badwuert-rad'";
    log badwuert-rad;
) &
wait ;

rm -f ./tmp/*

