#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math

from ngramm import NGramm, NGramms
from text import Text


class ParaphraseTest(object):

    def __init__(self, text1, text2):
        self.text1 = Text(text1)
        self.text2 = Text(text2)
        self.calculate_all_features()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'{0}\n{1}\nSLD: {SLD}, NG: {NG}, DS: {DS}, DC: {DC}, SNC: {SNC}\n'.format(
            unicode(self.text1),
            unicode(self.text2),
            SLD=self.sentence_length_difference,
            NG=self.ngramms_comparing,
            DS=self.dependencies_similarity,
            DC=self.dependencies_comparing,
            SNC=self.syntactic_ngramms_comparing
        )

    def calculate_all_features(self):
        self.calculate_sentence_length_difference()
        self.calculate_ngramms_comparing()
        self.calculate_dependencies_similarity()
        self.calculate_dependencies_comparing()
        self.calculate_syntactic_ngramms_comparing()

    # 1 feature SLD
    def calculate_sentence_length_difference(self):
        l1, l2 = len(self.text1.doc), len(self.text2.doc)
        # self.sentence_length_difference = float(l1 - l2) / l1
        self.sentence_length_difference = 1 / math.pow(0.8, l1 - l2)

    # 2 feature
    def calculate_ngramms_comparing(self):
        self.ngramms_comparing = []
        for i in range(1, 4):
            ngramms1 = NGramms(words=[t.text for t in self.text1.doc], n=i)
            ngramms2 = NGramms(words=[t.text for t in self.text2.doc], n=i)
            both = ngramms1.intersection(ngramms2)
            self.ngramms_comparing.append(float(len(both)) / len(ngramms1))

    # 3 feature DS
    def calculate_dependencies_similarity(self):
        value = 0.0
        for d in self.text1.deps:
            dep_d1 = self.get_connected_lexemes(d, self.text1.deps)
            dep_d2 = self.get_connected_lexemes(d, self.text2.deps)
            if len(dep_d1) and len(dep_d2):
                _max = max([self.sim(i, j) for i in dep_d1 for j in dep_d2])
                value += _max * self.brevity_penalty(len(dep_d1), len(dep_d2))
        value /= len(self.text1.deps) * self.brevity_penalty(len(self.text1.deps), len(self.text2.deps))
        self.dependencies_similarity = value

    # 4 feature DC
    def calculate_dependencies_comparing(self):
        intersection = 0.0
        for d1 in self.text1.deps:
            for d2 in self.text2.deps:
                if d1 == d2:
                    intersection += 1.0
        self.dependencies_comparing = intersection / len(self.text1.deps)

    # 5 feature syntactic NGramms comparing
    def calculate_syntactic_ngramms_comparing(self):
        self.syntactic_ngramms_comparing = []
        for i in range(2, 4):
            sngramms1 = self.text1.retrieve_syntactic_ngramms(i)
            sngramms2 = self.text2.retrieve_syntactic_ngramms(i)
            both = sngramms1.intersection(sngramms2)
            self.syntactic_ngramms_comparing.append(float(len(both)) / len(sngramms1))

    def get_connected_lexemes(self, d, deps):
        connected = []
        for item in deps:
            lexeme = item.getConnectedLexeme(d)
            if lexeme is not None:
                connected.append(lexeme)
        return connected

    def brevity_penalty(self, x, y):
        return 1 if y > x else math.pow(math.e, 1 - x/y)

    def sim(self, x, y):
        return x.similarity(y)
