# encoding: utf-8

import crossword

words = [
    u'でーた',
    u'こみっと',
    u'さーば',
    u'ばぶる',
    u'たぶれっと',
    u'れーるず',
    u'るーと',
]

crossword.build_crossword(6, 6, words, monitor={'EMPTY': u'＿', 'FILLED': u'凸'})
