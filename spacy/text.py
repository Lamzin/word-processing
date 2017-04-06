#!/usr/bin/python
# -*- coding: UTF-8 -*-

import spacy
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

    def retrieve_syntactic_ngramms(self, n):
        ngramms = []

        def dfs(root, stack):
            stack.append(root)
            if len(stack) >= n:
                ngramms.append(NGramm([token.text for token in stack[-n:]]))
            for child in root.children:
                dfs(child, stack)
            stack.pop()

        roots = {token.head: 0 for token in self.doc if token.dep == nsubj and token.head.pos == VERB}
        for root in roots:
            dfs(root, [])

        return NGramms(ngramms=ngramms)
