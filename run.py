# coding: utf-8

import random
import sys
import re
from codecs import open

import crossword2

with open(sys.argv[1], encoding='utf-8') as f:
    words = [s.strip() for s in f.readlines()]

if re.match('^[A-Za-z]*$', words[0]):
    dump_option = {'EMPTY': '_', 'FILLED': '#'}
else:
    dump_option = {'EMPTY': u'＿', 'FILLED': u'凸'}

random.shuffle(words)
crossword2.pickup_crosswords(words, dump_option=dump_option)
