#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import sets
from multiset import Multiset


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
        self.words = words

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        m = map(lambda s: u'"{}"'.format(unicode(s)), self.ngramms)
        return u', '.join(m)

    def __len__(self):
        return len(self.ngramms)

    def intersection(self, other):
        both = list(Multiset(self.ngramms).intersection(Multiset(other.ngramms)))
        return NGramms(ngramms=both)
