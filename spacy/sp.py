#!/usr/bin/python
# -*- coding: UTF-8 -*-

import spacy
import math
from spacy.symbols import nsubj, VERB


nlp = spacy.load('en')


class SyntaxDependency(object):

    def __init__(self, x, y, dep):
        self.x = x
        self.y = y
        self.dep = dep

    def getConnectedLexeme(self, dep):
        if (dep.x.text == self.y.text and dep.y.text != self.x.text) or (dep.y.text == self.y.text and dep.x.text != self.x.text):
            return self.x
        if (dep.x.text == self.x.text and dep.y.text != self.y.text) or (dep.y.text == self.x.text and dep.x.text != self.y.text):
            return self.y
        return None

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
        return unicode(self.text1) + u'\n' + unicode(self.text2)

    def calculate_all_features(self):
        self.dependencies_similarity()

    def dependencies_similarity(self):
        value = 0.0
        for d in self.text1.deps:
            dep_d1 = self.get_connected_lexemes(d, self.text1.deps)
            dep_d2 = self.get_connected_lexemes(d, self.text2.deps)
            _max = max([self.sim(i, j) for i in dep_d1 for j in dep_d2])
            value += _max * self.brevity_penalty(len(dep_d1), len(dep_d2))
        value /= len(self.text1.deps) * self.brevity_penalty(len(self.text1.deps), len(self.text2.deps))
        return value

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
    print ParaphraseTest(
        u'They had published an advertisement on the Internet on June 10, offering the cargo for sale, he added.',
        u'On June 10, the ship’s owners had published an advertisement on the Internet, offering the explosives for sale.',
    )