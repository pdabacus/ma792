#!/bin/bash
# prep.sh
# download and extract imdb data set and GloVe 6B word vectors

imdb_url="http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
imdb_md5="7c2ac02c03563afcf9b574c7e56c153a"
imdb_out="downloads/imdb.tar.gz"
imdb_outdir="aclImdb"
imdb_outdir2="imdb"

glove_url="http://nlp.stanford.edu/data/glove.6B.zip"
glove_md5="056ea991adb4740ac6bf1b6d9b50408b"
glove_out="downloads/glove.6B.zip"
glove_file_out="glove.6B.100d.txt"
glove_outdir="glove"

if ! [ -d "downloads" ]; then
    mkdir -p "downloads"
fi

if [ -f "$imdb_out" ]; then
    m=$(md5sum "$imdb_out" | awk '{print $1}')
    if [ $m = $imdb_md5 ]; then
        echo "using downloaded dataset $imdb_out"
    else
        echo "redownloading dataset"
        curl -L "$imdb_url" -o "$imdb_out"
    fi
else
    echo "downloading imdb dataset"
    curl -L "$imdb_url" -o "$imdb_out"
fi

echo "extracting imdb dataset to $imdb_outdir/"
rm -rf "$imdb_outdir" "$imdb_outdir2"
tar -zxf "$imdb_out" -C .
mv "$imdb_outdir" "$imdb_outdir2"

echo "removing unneeded train/unsup directory"
rm -rf "$imdb_outdir2/train/unsup"

head -n 15 "$imdb_outdir2/README"
echo

du -sh "$imdb_outdir2"

echo
echo "################"
echo

if [ -f "$glove_out" ]; then
    m=$(md5sum "$glove_out" | awk '{print $1}')
    if [ $m = $glove_md5 ]; then
        echo "using downloaded model $glove_out"
    else
        echo "redownloading model"
        curl -L "$glove_url" -o "$glove_out"
    fi
else
    echo "downloading glove model"
    curl -L "$glove_url" -o "$glove_out"
fi

echo "extracting glove model to $glove_outdir/"
rm -rf "$glove_outdir"
unzip "$glove_out" "$glove_file_out" -d "$glove_outdir"
echo

du -sh "$glove_outdir"
