#!/usr/bin/python
# -*- coding: UTF-8 -*-

import spacy
import math
import hashlib
import sets
from spacy.symbols import nsubj, VERB


nlp = spacy.load('en')


class SyntaxDependency(object):

    def __init__(self, x, y, dep):
        self.x = x
        self.y = y
        self.dep = dep

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"{0} <--- {1} ---> {2}".format(self.x.text, self.dep, self.y.text)

    def __eq__(self, other):
        return self.x.text == other.x.text and \
               self.y.text == other.y.text and \
               self.dep == other.dep

    def getConnectedLexeme(self, dep):
        if (dep.x.text == self.y.text and dep.y.text != self.x.text) or \
           (dep.y.text == self.y.text and dep.x.text != self.x.text):
            return self.x
        if (dep.x.text == self.x.text and dep.y.text != self.y.text) or \
           (dep.y.text == self.x.text and dep.x.text != self.y.text):
            return self.y
        return None


class NGramm(object):

    def __init__(self, words):
        self.words = words;

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u' '.join(self.words)

    def __hash__(self):
        return hash(u' | '.join(self.words))

    def __len__(self):
        return len(self.words)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self.words[i] != other.words[i]:
                return False
        return True

    def __ne__(self, other):
        return (not self.__eq__(other))


class NGramms(object):

    def __init__(self, words=None, n=None, ngramms=None):
        if ngramms is not None:
            self.ngramms = ngramms
            return
        self.ngramms = [NGramm(words[i:i+n]) for i in range(len(words)-n)]
        self.ngramms = list(sets.Set(self.ngramms))
        self.words = words

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        m = map(lambda s: u'"{}"'.format(unicode(s)), self.ngramms)
        return u', '.join(m)

    def __len__(self):
        return len(self.ngramms)

    def intersection(self, other):
        both = list(sets.Set(self.ngramms).intersection(sets.Set(other.ngramms)))
        return NGramms(ngramms=both)


class Text(object):

    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)
        self.retrieve_dependencies()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.text

    def retrieve_dependencies(self):
        'return list of all syntax dependencies in document'
        verbs = {token.head: 0 for token in self.doc if token.dep == nsubj and token.head.pos == VERB}
        i = 0
        self.deps = []
        queue = [k for k in verbs.keys()]
        while i < len(queue):
            for child in queue[i].children:
                queue.append(child)
                self.deps.append(SyntaxDependency(queue[i], child, child.dep_))
            i += 1


class ParaphraseTest(object):

    def __init__(self, text1, text2):
        self.text1 = Text(text1)
        self.text2 = Text(text2)
        self.calculate_all_features()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'{0}\n{1}\nSLD: {SLD}, NG: {NG}, DS: {DS}, DC: {DC}\n'.format(
            unicode(self.text1),
            unicode(self.text2),
            SLD=self.sentence_length_difference,
            NG=self.ngramms_comparing,
            DS=self.dependencies_similarity,
            DC=self.dependencies_comparing,
        )

    def calculate_all_features(self):
        self.calculate_sentence_length_difference()
        self.calculate_ngramms_comparing()
        self.calculate_dependencies_similarity()
        self.calculate_dependencies_comparing()

    # 1 feature SLD
    def calculate_sentence_length_difference(self):
        l1, l2 = len(self.text1.doc), len(self.text2.doc)
        self.sentence_length_difference = float(l1 - l2) / l1

    # 2 feature
    def calculate_ngramms_comparing(self):
        self.ngramms_comparing = []
        # for i in range(1, 4):
        for i in range(1, 2):
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


if __name__ == "__main__":
    sentence1 = u'They had published an advertisement on the Internet on June 10, offering the cargo for sale, he added.'
    sentence2 = u'On June 10, the ship’s owners had published an advertisement on the Internet, offering the explosives for sale.'

    print ParaphraseTest(sentence1, sentence1)
    # print ParaphraseTest(sentence1, sentence2)
    # print ParaphraseTest(sentence2, sentence1)
