#!/bin/sh

function copy {
    pv ./output/$1.img > /media/garmin-sd/GARMIN/$1.img &&
    echo -e "`date +%d.%m.%Y\ %H:%M`: copied $1\n$(cat updates)" > updates ;
}

copy bw;
copy deutschland;
copy badwuert-rad;
copy TK-DACH-Wanderwege;

