#!/bin/bash

# fetch saxon-he-12.3.jar.
if [ ! -f saxon/saxon-he-12.3.jar ]; then
    echo "hello"
    mkdir -p saxon
    cd saxon
    wget https://github.com/Saxonica/Saxon-HE/releases/download/SaxonHE12-3/SaxonHE12-3J.zip
    unzip SaxonHE12-3J.zip
    cd ..
fi

# run scripts
python3 ./bnfa/scripts/transform.py

