#!/usr/bin/python
# -*- coding: UTF-8 -*-

from paraphrase import ParaphraseTest

def test(s1, s2, is_paraphrase):
    print('Paraphrase: ' if is_paraphrase else 'Not paraphrase: ')
    print(ParaphraseTest(s1, s2))
    print(ParaphraseTest(s2, s1))
    print('')

if __name__ == "__main__":
    test(
        u'They had published an advertisement on the Internet on June 10, offering the cargo for sale, he added.',
        u'On June 10, the ship’s owners had published an advertisement on the Internet, offering the explosives for sale.',
        True
    )

    test(
        u'Yucaipa owned Dominick’s before selling the chain to Safeway in 1998 for $2.5 billion.',
        u'Yucaipa bought Dominick’s in 1995 for $693 million and sold it to Safeway for $1.8 billion in 1998.',
        False
    )

    test(
        u'I study english to work at Google in Canada.',
        u'I have never been in London.',
        False
    )
