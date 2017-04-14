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
