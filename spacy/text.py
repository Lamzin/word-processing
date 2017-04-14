#!/usr/bin/python
# -*- coding: UTF-8 -*-

import spacy
from multiset import Multiset
from spacy.symbols import nsubj, VERB
from syntax_dependency import SyntaxDependency
from ngramm import NGramm, NGramms


nlp = spacy.load('en')


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
        'return list of all alphabetical syntax dependencies in document'
        self.deps = []
        for token in self.doc:
            if not token.is_alpha:
                continue
            for child in token.children:
                if not child.is_alpha:
                    continue
                self.deps.append(SyntaxDependency(token, child, child.dep_))
        self.deps = Multiset(self.deps)

    def retrieve_syntactic_ngramms(self, n):
        ngramms = []
        if n == 1:
            ngramms = [NGramm([token.text]) for token in self.doc if token.is_alpha]
        elif n == 2:
            for token in self.doc:
                if not token.is_alpha:
                    continue
                for child in token.children:
                    if not child.is_alpha:
                        continue
                    ngramms.append(NGramm([token.text, child.text]))
        elif n == 3:
            for token in self.doc:
                if not token.is_alpha:
                    continue
                children = [ch for ch in token.children]
                for i in range(len(children)):
                    if not children[i].is_alpha:
                        continue
                    for j in range(i + 1, len(children)):
                        if not children[j].is_alpha:
                            continue
                        ng = NGramm([token.text, children[i].text, children[j].text])
                        ngramms.append(ng)
            for token in self.doc:
                if not token.is_alpha:
                    continue
                for ch1 in token.children:
                    if not ch1.is_alpha:
                        continue
                    for ch2 in token.children:
                        if not ch2.is_alpha:
                            continue
                        ng = NGramm([token.text, ch1.text, ch2.text])
                        ngramms.append(ng)
        ngramms = Multiset(ngramms)
        return NGramms(ngramms=ngramms)
