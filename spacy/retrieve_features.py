#!/usr/bin/python
# -*- coding: UTF-8 -*-


import synonyms
import extractor
import pickle

from paraphrase import ParaphraseTest


class Train(object):
    def __init__(self, is_paraphrase, id1, id2, s1, s2):
        self.id1 = id1
        self.id2 = id2
        self.s1 = s1
        self.s2 = s2
        self.is_paraphrase = is_paraphrase

    def run(self):
        self.features = ParaphraseTest(self.s1, self.s2).get_features()

    def __str__(self):
        return '{0}: {1}'.format(self.is_paraphrase, self.features)


if __name__ == "__main__":
    trains = extractor.get_all_trains()
    trains = [Train(t[0], t[1], t[2], t[3], t[4]) for t in trains]

    for i, t in enumerate(trains):
        t.run()
        print "{}/{}: {}".format(i, len(trains), t)

    with open('train.pkl', 'wb') as output:
        pickle.dump(trains, output, pickle.HIGHEST_PROTOCOL)
