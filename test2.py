# coding: utf-8

import random

import crossword2

with open('words') as f:
    words = [s.strip() for s in f.readlines()]

random.shuffle(words)
crossword2.pickup_crosswords(words, monitor=True)
