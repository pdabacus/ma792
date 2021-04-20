"""
build dictionary of word vectors in memory from GloVe
"""
import os
import sys
import numpy as np

_version = "1.0.0"
_file = "glove/glove.6B.100d.txt"

class GloVe():
    _embed = None
    _vectors = None

    def __init__(self, file=_file):
        self._file = file
        self._embed = dict()
        self._vectors = list()
        print("building word embedding from %s" % file)
        f = open(file, "r")
        index = 0
        for line in f:
            key, *vec = line.split()
            self._embed[key] = index
            self._vectors.append(np.asarray(vec, dtype="float32"))
            index += 1
        f.close()

        print("built embedding of %d word vectors each of length %d"
            % (len(self._vectors), len(vec))
        )

    def wordvec(self, word):
        "find the vector for a given word"
        v_id = self._embed.get(word.lower(), None)
        if v_id is None:
            v_id = self._embed["the"]
        return self._vectors[v_id]

    def nearest(self, wordvec, n=1):
        words = ["dog"]*n    # list of nearest words from best to worst
        dists = [6.022e23]*n # list of distances smallest to largest
        for word, vec_id in self._embed.items():
            vec = self._vectors[vec_id]
            d = np.linalg.norm(vec - wordvec)
            if (d < dists[-1]):
                insert_index = n-1
                while (insert_index >= 1) and (d < dists[insert_index-1]):
                    insert_index -= 1
                for j in range(1, n - insert_index):
                    words[-j] = words[-j-1]
                    dists[-j] = dists[-j-1]
                words[insert_index] = word
                dists[insert_index] = d
        if n == 1:
            return words[0]
        else:
            return words

    def encode(self, processed_sentence, final_length):
        n = len(processed_sentence)
        r = [self._embed.get(w, 0) for w in processed_sentence]
        if n < final_length:
            r += [0]* (final_length-n)
        else:
            r = r[:final_length]
        return r


def main():
    g = GloVe(_file)

    print()
    print("king is to queen as boy is to:")
    king = g.wordvec("king")
    queen = g.wordvec("queen")
    boy = g.wordvec("boy")

    wordvec = boy + (queen-king)
    word = g.nearest(wordvec, 5)
    print(word)

    print()
    print("synonyms of stupid:")
    words = g.nearest(g.wordvec("stupid"), 11)[1:]
    print(words)

if __name__ == "__main__":
    main()
