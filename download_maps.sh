#!/bin/sh

mkdir -p tmp
rm -f ./tmp/*

(
    wget -P ./tmp/ http://osm.thkukuk.de/TK-DACH-Wanderwege.7z;
    echo "Downloaded 'Wanderwege'";
    7z e -aoa ./tmp/TK-DACH-Wanderwege.7z -otmp/;
    mv ./tmp/TK-DACH-Wanderwege.img ./output/;
    echo "Done with 'Wanderwege'";
    echo -e "`date +%d.%m.%Y`: downloaded TK-DACH-Wanderwege\n$(cat updates)" > updates ;
) &
(
    wget -P ./tmp/ http://gps.maroufi.net/download/badwuert-rad.img;
    echo "Downloaded 'badwuert-rad'";
    cp ./tmp/badwuert-rad.img ./output/;
    echo "Done with 'badwuert-rad'";
    echo -e "`date +%d.%m.%Y`: downloaded badwuert-rad\n$(cat updates)" > updates ;
) &
wait ;

rm -f ./tmp/*

