# encoding: utf-8

import random

import crossword2

words = [
    u'でーた',
    u'こみっと',
    u'さーば',
    u'ばぶる',
    u'たぶれっと',
    u'れーるず',
    u'るーと',
    u'こみゅにてぃ',
    u'どっとねっと',
    u'うぇぶ',
    u'くらうど',
    u'でべろっぱ',
    u'さーびす',
    u'あじゃいる',
    u'えんぷら',
    u'あーきてくちゃ',
]

random.shuffle(words)
#crossword2.pickup_crosswords(words, monitor={'EMPTY': u'＿', 'FILLED': u'凸'})
crossword2.pickup_crosswords(words, dump_option={'EMPTY': u'＿', 'FILLED': u'凸'})
