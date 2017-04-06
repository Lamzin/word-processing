#!/usr/bin/python
# -*- coding: UTF-8 -*-


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
