#!/bin/bash
# download.sh
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

py1_url="https://raw.githubusercontent.com/pdabacus/ma792/main/glove.py"
py1_md5="af82391c9585b248c2f3510024f04e2f"
py1_out="glove.py"

py2_url="https://raw.githubusercontent.com/pdabacus/ma792/main/imdb.py"
py2_md5="ec433bdc266a4733b3f4c663a2f4663d"
py2_out="imdb.py"

py3_url="https://raw.githubusercontent.com/pdabacus/ma792/main/rnn.py"
py3_md5="2d568e56d1979ab417977814ff828ac4"
py3_out="rnn.py"

rnn_url="https://github.com/pdabacus/ma792/releases/download/v1.1/happy_angry_rnn.pt"
rnn_md5="d108bc7e670151b664ec24957805c2b7"
rnn_out="happy_angry_rnn.pt"

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

echo
echo "################"
echo

if [ -f "$py1_out" ]; then
    m=$(md5sum "$py1_out" | awk '{print $1}')
    if [ $m = $py1_md5 ]; then
        echo "using downloaded code $py1_out"
    else
        echo "redownloading code"
        curl -L "$py1_url" -o "$py1_out"
    fi
else
    echo "downloading code $py1_out"
    curl -L "$py1_url" -o "$py1_out"
fi

echo
echo "################"
echo

if [ -f "$py2_out" ]; then
    m=$(md5sum "$py2_out" | awk '{print $1}')
    if [ $m = $py2_md5 ]; then
        echo "using downloaded code $py2_out"
    else
        echo "redownloading code"
        curl -L "$py2_url" -o "$py2_out"
    fi
else
    echo "downloading code $py2_out"
    curl -L "$py2_url" -o "$py2_out"
fi

echo
echo "################"
echo

if [ -f "$py3_out" ]; then
    m=$(md5sum "$py3_out" | awk '{print $1}')
    if [ $m = $py3_md5 ]; then
        echo "using downloaded code $py3_out"
    else
        echo "redownloading code"
        curl -L "$py3_url" -o "$py3_out"
    fi
else
    echo "downloading code $py3_out"
    curl -L "$py3_url" -o "$py3_out"
fi

echo
echo "################"
echo

if [ -f "$rnn_out" ]; then
    m=$(md5sum "$rnn_out" | awk '{print $1}')
    if [ $m = $rnn_md5 ]; then
        echo "using downloaded pytorch model $rnn_out"
    else
        echo "redownloading pytorch model"
        curl -L "$rnn_url" -o "$rnn_out"
    fi
else
    echo "downloading pytorch model $rnn_out"
    curl -L "$rnn_url" -o "$rnn_out"
fi

echo
echo "finished downloading needed data"
