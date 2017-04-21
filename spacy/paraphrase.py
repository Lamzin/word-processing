#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import extractor
import sets

from ngramm import NGramm, NGramms
from nltk.text import TextCollection
from text import Text

import synonyms


texts_corpus = TextCollection(extractor.get_all_sentenses())


class ParaphraseTest(object):

    def __init__(self, text1, text2):
        self._idf_matches_cache = {}
        self.text1 = Text(text1)
        self.text2 = Text(text2)
        self.calculate_all_features()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'{0}\n{1}\nSLD: {SLD}, NG: {NG}, DS: {DS}, DC: {DC}, SNC: {SNC}, BLEU: {BLEU}, IDF_BLEU: {IDF_BLEU}, SBLEU: {SBLEU}, NIST: {NIST}\n'.format(
            unicode(self.text1),
            unicode(self.text2),
            SLD=self.sentence_length_difference,
            NG=self.ngramms_comparing,
            DS=self.dependencies_similarity,
            DC=self.dependencies_comparing,
            SNC=self.syntactic_ngramms_comparing,
            BLEU=self.bleu,
            IDF_BLEU = self.idf_bleu,
            SBLEU = self.sbleu,
            NIST = self.nist
        )

    def get_features(self):
        features = []
        features.append(self.sentence_length_difference)
        features.extend(self.ngramms_comparing)
        features.append(self.dependencies_similarity)
        features.append(self.dependencies_comparing)
        features.extend(self.syntactic_ngramms_comparing)
        features.append(self.bleu)
        features.append(self.idf_bleu)
        features.append(self.sbleu)
        features.append(self.nist)
        return features

    def calculate_all_features(self):
        self.calculate_sentence_length_difference()
        self.calculate_ngramms_comparing()
        self.calculate_dependencies_similarity()
        self.calculate_dependencies_comparing()
        self.calculate_syntactic_ngramms_comparing()
        self.calculate_bleu()
        self.calculate_idf_bleu()
        self.calculate_sbleu()
        self.calculate_nist()

    # 1 feature SLD
    def calculate_sentence_length_difference(self):
        l1, l2 = len(self.text1.doc), len(self.text2.doc)
        self.sentence_length_difference = 1 / math.pow(0.8, l1 - l2)

    # 2 feature
    def calculate_ngramms_comparing(self):
        self.ngramms_comparing = []
        for i in range(1, 4):
            ngramms1 = NGramms(words=[t.text for t in self.text1.doc if t.is_alpha], n=i)
            ngramms2 = NGramms(words=[t.text for t in self.text2.doc if t.is_alpha], n=i)
            both = ngramms1.intersection(ngramms2)
            self.ngramms_comparing.append(float(both.count()) / ngramms1.count())

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
                if synonyms.is_equal([d1.x.text, d1.y.text], [d2.x.text, d2.y.text]):
                    intersection += 1.0
                if synonyms.is_equal([d1.x.text, d1.y.text], [d2.x.text, d2.y.text]) and not d1 == d2:
                    # case when dependencies look like synonyms
                    pass
        self.dependencies_comparing = intersection / len(self.text1.deps)

    # 5 feature syntactic NGramms comparing
    def calculate_syntactic_ngramms_comparing(self):
        self.syntactic_ngramms_comparing = []
        for i in range(2, 4):
            sngramms1 = self.text1.retrieve_syntactic_ngramms(i)
            sngramms2 = self.text2.retrieve_syntactic_ngramms(i)
            both = sngramms1.intersection(sngramms2)
            self.syntactic_ngramms_comparing.append(float(both.count()) / sngramms1.count())

    # 6 BLEU
    def calculate_bleu(self):
        def precision(n):
            ngramms1 = NGramms(words=[t.text for t in self.text1.doc if t.is_alpha], n=n)
            ngramms2 = NGramms(words=[t.text for t in self.text2.doc if t.is_alpha], n=n)
            both = ngramms1.intersection(ngramms2)
            numerator, denominator = 0.000001, 0.000001
            for x in ngramms2.ngramms:
                numerator += both.ngramms[x]
                denominator += ngramms2.ngramms[x]
            return numerator / denominator

        N = 3
        bp = self.brevity_penalty(len(self.text1.doc), len(self.text2.doc))
        self.bleu = bp * math.exp(sum(math.log(precision(i))/N for i in range(1, N + 1)))

    # 7 IDF BLEU
    def calculate_idf_bleu(self):
        def precision(n):
            ngramms1 = NGramms(words=[t.text for t in self.text1.doc if t.is_alpha], n=n)
            ngramms2 = NGramms(words=[t.text for t in self.text2.doc if t.is_alpha], n=n)
            both = ngramms1.intersection(ngramms2)
            numerator, denominator = 0.000001, 0.000001
            for x in ngramms2.ngramms:
                if self.idf(x.words) > 5:
                    numerator += both.ngramms[x]
                    denominator += ngramms2.ngramms[x]
            return numerator / denominator

        N = 3
        bp = self.brevity_penalty(len(self.text1.doc), len(self.text2.doc))
        self.idf_bleu = bp * math.exp(sum(math.log(precision(i))/N for i in range(1, N + 1)))

    # 8 SyntaxBLEU - using syntax Ngramm
    def calculate_sbleu(self):
        def precision(n):
            sngramms1 = self.text1.retrieve_syntactic_ngramms(n)
            sngramms2 = self.text2.retrieve_syntactic_ngramms(n)
            both = sngramms1.intersection(sngramms2)
            numerator, denominator = 0.000001, 0.000001
            for x in sngramms2.ngramms:
                numerator += both.ngramms[x]
                denominator += sngramms2.ngramms[x]
            return numerator / denominator

        N = 3
        bp = self.brevity_penalty(len(self.text1.doc), len(self.text2.doc))
        self.sbleu = bp * math.exp(sum(math.log(precision(i))/N for i in range(1, N + 1)))

    # 9 NIST
    def calculate_nist(self):
        self.nist = 0.0
        for i in range(2, 4):
            ngramms = NGramms(words=[t.text for t in self.text1.doc if t.is_alpha], n=i)
            for ng in ngramms.ngramms:
                self.nist += self.idf(ng.words) / ngramms.ngramms[ng]
        self.nist *= self.brevity_penalty(len(self.text1.doc), len(self.text2.doc))

    def idf(self, words):

        def _idf(word):
            m = self._idf_matches_cache.get(word)
            if m is not None:
                return m
            m = {i for i, text in enumerate(texts_corpus._texts) if word in text}
            self._idf_matches_cache[word] = m
            return m

        matches = _idf(words[0])
        for word in words[1:]:
            matches = matches.intersection(_idf(word))
        return math.log(float(len(texts_corpus._texts)) / len(matches)) if matches else 0.0

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
