#!/usr/bin/python
# -*- coding: UTF-8 -*-


def get_all_sentenses():
    file = open('msrpc/msr_paraphrase_data.txt')
    lines = file.xreadlines()

    texts = []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        rows = line.split('\t')
        texts.append(rows[1].decode('utf-8'))
    return texts


def get_all_trains():
    return _get_pairs('msrpc/msr_paraphrase_train.txt')


def get_all_tests():
    return _get_pairs('msrpc/msr_paraphrase_test.txt')


def _get_pairs(file_name):
    file = open(file_name)
    lines = file.xreadlines()

    tests = []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        rows = [item.decode('utf-8') for item in  line.split('\t')]
        tests.append([rows[0] == u'1', rows[1], rows[2], rows[3], rows[4]])
    return tests
