#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sets

from nltk.corpus import wordnet


def get_synonyms(word):
    synonyms = sets.Set()
    synonyms.add(word)
    for ss in wordnet.synsets(word):
        for lemma in ss.lemma_names():
            synonyms.add(lemma)
    return synonyms


def is_equal(sequence1, sequence2):
    if len(sequence1) != len(sequence2):
        return False

    def dfs(prev, i, sequence, stack, candidates):
        stack.append(prev)
        if i == len(sequence):
            candidates.add(' + '.join(sorted(stack[1:])))
            stack.pop()
            return
        for s in get_synonyms(sequence[i]):
            dfs(s, i+1, sequence, stack, candidates)
        stack.pop()

    candidates1, candidates2 = sets.Set(), sets.Set()
    dfs('', 0, sequence1, [], candidates1)
    dfs('', 0, sequence2, [], candidates2)

    return len(candidates1.intersection(candidates2)) > 0
