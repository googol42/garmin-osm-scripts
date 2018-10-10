#!/bin/sh

language="de";
cores=4;
ram=5000;
style="my-outdoor.TYP"

# TODO add a check if we have to call bootstrap

function build {
    cd ./fzk-mde-garmin/Freizeitkarte-Entwicklung/ ;
    perl mt.pl --language=$language --cores=$cores --ram=$ram create     $1 ;
    perl mt.pl --language=$language --cores=$cores --ram=$ram fetch_osm  $1 ;
    perl mt.pl --language=$language --cores=$cores --ram=$ram fetch_ele  $1 ;
    perl mt.pl --language=$language --cores=$cores --ram=$ram join       $1 ;
    perl mt.pl --language=$language --cores=$cores --ram=$ram split      $1 ;
    # build standard map
    perl mt.pl --language=$language --cores=$cores --ram=$ram build      $1 $3 ;
    perl mt.pl --language=$language --cores=$cores --ram=$ram gmapsupp   $1 ;
    moveMap $1 $2.img ;
    applyStyle $2.img ;
    # Build expore map
    perl mt.pl --language=$language --cores=$cores --ram=$ram build      $1 DEXPLORE $3 ;
    perl mt.pl --language=$language --cores=$cores --ram=$ram gmapsupp   $1 ;
    moveMap $1 $2-explore.img;
    applyStyle $2-explore.img;
    cd ../..;
    echo -e "`date +%d.%m.%Y\ %H:%M`: built $2\n$(cat updates)" > updates ;
}

function moveMap {
    mv ./install/$1_$language/gmapsupp.img ../../output/$2 ;
}

function applyStyle {
    cd ../../ReplaceTyp/ ;
    ./ReplaceTyp.sh ../output/$1 $style ;
    cd ../fzk-mde-garmin/Freizeitkarte-Entwicklung/ ;
}

# build Freizeitkarte_IRL ireland;
# build Freizeitkarte_SAARLAND saarland;
# build Freizeitkarte_ALPS alps DEXTENDEDROUTING ;
build Freizeitkarte_BADEN-WUERTTEMBERG bw ;
# build Freizeitkarte_DEU deutschland ;
# build Freizeitkarte_CHE ch ;
# build Freizeitkarte_AUT at ;

