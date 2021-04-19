"""
read in imdb reviews and preprocess by removing symbols and stopwords
"""

import os
import sys
import re
import random

_version = "1.0.0"
_folder = "imdb"

_stopwords = {"a","about","above","after","again","against","all","am","an","and","any","are",
    "arent","as","at","be","because","been","before","being","below","between","both","but","by",
    "cant","cannot","could","couldnt","did","didnt","do","does","doesnt","doing","dont","down",
    "during","each","few","for","from","further","had","hadnt","has","hasnt","have","havent",
    "having","he","hed","hell","hes","her","here","heres","hers","herself","him","himself","his",
    "how","hows","i","id","ill","im","ive","if","in","into","is","isnt","it","its","its","itself",
    "lets","me","more","most","mustnt","my","myself","no","nor","not","of","off","on","once",
    "only","or","other","ought","our","ours","ourselves","out","over","own","same","shant","she",
    "shed","shell","shes","should","shouldnt","so","some","such","than","that","thats","the",
    "their","theirs","them","themselves","then","there","theres","these","they","theyd","theyll",
    "theyre","theyve","this","those","through","to","too","under","until","up","very","was",
    "wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where",
    "wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt",
    "you","youd","youll","youre","youve","your","yours","yourself","yourselves"
} # 174 words from https://www.ranks.nl/stopwords

_html_tags = re.compile(r"<.+?/>")
_nonstd_chars = re.compile(r"[^\w\s]")
_digits = re.compile(r"\d")
_multiple_spaces = re.compile(r"\s+")

class IMDB():
    _pos = list()
    _neg = list()

    def __init__(self, folder=_folder):
        self._folder = folder
        print("preprocessing reviews from %s/train/pos" % folder)
        train_pos = [folder + "/train/pos/" + j for j in os.listdir(folder + "/train/pos")]
        n = len(train_pos)
        jp = 0
        print("[" + 20*" " + "]", end="\r[", flush=True)
        for j in range(n):
            f = open(train_pos[j], "r")
            txt = f.read()
            f.close()
            self._pos.append(self.process(txt))
            if j > jp*n/20:
                jp += 1
                print("*", end="", flush=True)
        print("] %d/%d" % (n,n))

        print("preprocessing reviews from %s/test/pos" % folder)
        test_pos = [folder + "/test/pos/" + j for j in os.listdir(folder + "/test/pos")]
        n = len(test_pos)
        jp = 0
        print("[" + 20*" " + "]", end="\r[", flush=True)
        for j in range(n):
            f = open(test_pos[j], "r")
            txt = f.read()
            f.close()
            self._pos.append(self.process(txt))
            if j > jp*n/20:
                jp += 1
                print("*", end="", flush=True)
        print("] %d/%d" % (n,n))

        print("preprocessing reviews from %s/train/neg" % folder)
        train_neg = [folder + "/train/neg/" + j for j in os.listdir(folder + "/train/neg")]
        n = len(train_neg)
        jp = 0
        print("[" + 20*" " + "]", end="\r[", flush=True)
        for j in range(n):
            f = open(train_neg[j], "r")
            txt = f.read()
            f.close()
            self._neg.append(self.process(txt))
            if j > jp*n/20:
                jp += 1
                print("*", end="", flush=True)
        print("] %d/%d" % (n,n))

        print("preprocessing reviews from %s/test/neg" % folder)
        test_neg = [folder + "/test/neg/" + j for j in os.listdir(folder + "/test/neg")]
        n = len(test_neg)
        jp = 0
        print("[" + 20*" " + "]", end="\r[", flush=True)
        for j in range(n):
            f = open(test_neg[j], "r")
            txt = f.read()
            f.close()
            self._neg.append(self.process(txt))
            if j > jp*n/20:
                jp += 1
                print("*", end="", flush=True)
        print("] %d/%d" % (n,n))

    @staticmethod
    def process(txt):
        "remove all stop words and non-alphabet symbols"
        s = _html_tags.sub(" ", txt)
        s = _nonstd_chars.sub("", s)
        s = _digits.sub(" ", s)
        s = _multiple_spaces.sub(" ", s)
        words = s.lower().strip().split()
        return list(filter(lambda x: x not in _stopwords, words))

    def pos(self, j=-1):
        "get a positive review randomly or at specified index"
        if j < 0:
            j = random.randint(0,len(self._pos)-1)
        return self._pos[j]

    def neg(self, j=-1):
        "get a negative review randomly or at specified index"
        if j < 0:
            j = random.randint(0,len(self._neg)-1)
        return self._neg[j]

def main():
    imdb = IMDB(_folder)
    print("positive review:")
    print(imdb.pos())

if __name__ == "__main__":
    main()
