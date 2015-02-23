# coding: utf-8

import re

from crossword import *


class Crossword2(Crossword):

    def __init__(self):
        self.grid = OpenGrid()
        self.connected = {}
        self.used_words = []

    def copy(self):
        copied = Crossword2()
        copied.grid = self.grid.copy()
        copied.connected = self.connected.copy()
        copied.used_words = self.used_words[:]
        return copied

    def embed(self, pos, direction, word):
        assert word not in self.used_words
        super(Crossword2, self).embed(pos, direction, word)
        self.used_words.append(word)

    def all_disconnected_sequences(self):
        '''
        >>> c = Crossword2()
        >>> c.embed((0, 0), HORIZONTAL, 'ANT')
        >>> c.embed((0, 0), VERTICAL, 'ATOM')
        >>> c.embed((1, 2), HORIZONTAL, 'IT')
        >>> c.embed((3, 0), HORIZONTAL, 'MEET')
        >>> c.dump()
        _#____
        #ANT#_
        _T#IT#
        _O____
        #MEET#
        _#____
        >>> c.all_disconnected_sequences()
        [((0, 2), 2, 'T'), ((1, 0), 2, 'T'), ((2, 0), 2, 'O'), ((0, 1), 1, 'N'), ((3, 1), 1, 'E'), ((0, 2), 1, 'TI'), ((0, 2), 1, 'TI.E'), ((3, 2), 1, 'E'), ((1, 3), 1, 'T'), ((1, 3), 1, 'T.T'), ((3, 3), 1, 'T')]

        '''
        sequences = []
        for pos, direction, length in [((r, self.grid.colmin), HORIZONTAL, self.grid.width) for r in range(self.grid.rowmin, self.grid.rowmax + 1)] + [((self.grid.rowmin, c), VERTICAL, self.grid.height) for c in range(self.grid.colmin, self.grid.colmax + 1)]:
            line = self.grid.get_word(pos, direction, length)
            poslist = self.grid.poslist(pos, direction, length)
            sequences += self.extract_sequences(line, poslist, direction)
        return [(p, d, w) for (p, d, w) in sequences if not w.endswith('.')]

    def extract_sequences(self, line, poslist, direction, idx=0, current_seq=None):
        '''
        >>> c = Crossword2()
        >>> c.extract_sequences('ABC', [(0, 0), (0, 1), (0, 2)], HORIZONTAL)
        [((0, 0), 2, 'ABC')]
        >>> c.extract_sequences('_A_', [(0, 0), (0, 1), (0, 2)], HORIZONTAL)
        [((0, 1), 2, 'A'), ((0, 1), 2, 'A.')]
        >>> c.extract_sequences('A_C', [(0, 0), (0, 1), (0, 2)], HORIZONTAL)
        [((0, 0), 2, 'A'), ((0, 0), 2, 'A.C'), ((0, 2), 2, 'C')]
        >>> c.extract_sequences('A#C', [(0, 0), (0, 1), (0, 2)], HORIZONTAL)
        [((0, 0), 2, 'A'), ((0, 2), 2, 'C')]
        >>> c.extract_sequences('A_#B_C', [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0,5)], HORIZONTAL)
        [((0, 0), 2, 'A'), ((0, 0), 2, 'A.'), ((0, 3), 2, 'B'), ((0, 3), 2, 'B.C'), ((0, 5), 2, 'C')]
        >>> c.extract_sequences('A_B__C', [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0,5)], HORIZONTAL)
        [((0, 0), 2, 'A'), ((0, 0), 2, 'A.B'), ((0, 2), 2, 'B'), ((0, 0), 2, 'A.B.'), ((0, 2), 2, 'B.'), ((0, 0), 2, 'A.B..C'), ((0, 2), 2, 'B..C'), ((0, 5), 2, 'C')]
        '''
        if not current_seq: current_seq = []
        if idx >= len(line): return current_seq
        c = line[idx]
        pos = poslist[idx]

        if c == FILLED:
            return current_seq + self.extract_sequences(line, poslist, direction, idx + 1, [])
        if c == EMPTY:
            new_current_seq = [(p, d, s + '.') for (p, d, s) in current_seq]
            return current_seq + self.extract_sequences(line, poslist, direction, idx + 1, new_current_seq)

        if current_seq:
            new_current_seq = [(p, d, s + c) for (p, d, s) in current_seq if not self.is_connected(poslist[idx - 1], pos)]
            if any([s.endswith('.') for (p, d, s) in current_seq]):
                new_current_seq.append((pos, direction, c))
            return self.extract_sequences(line, poslist, direction, idx + 1, new_current_seq)
        else:
            new_current_seq = [(pos, direction, c)]
            return self.extract_sequences(line, poslist, direction, idx + 1, new_current_seq)


def build_crossword2(words, monitor=False):
    '''
    >>> ans = build_crossword2(['ANT', 'ART', 'RAT'])
    >>> for a in ans: a.dump()
    #ANT#
    _#___
    #ANT#
    _R___
    _T___
    _#___
    ___#___
    __#ANT#
    ___R___
    #RAT#__
    ___#___
    ___#_
    ___R_
    _#_A_
    #ANT#
    _R_#_
    _T___
    _#___
    _#___
    _R___
    #ANT#
    _T___
    _#___
    ___#_
    _#_A_
    _R_R_
    #ANT#
    _T_#_
    _#___
    ___#___
    ___R___
    __#ANT#
    #ART#__
    ___#___
    ___#_
    ___A_
    ___R_
    #ANT#
    ___#_
    ___#__
    _#RAT#
    ___R__
    #ANT#_
    ___#__
    ___#_
    _#_A_
    _R_R_
    #ANT#
    _T_#_
    _#___
    ___#___
    ___A___
    __#RAT#
    #ANT#__
    ___#___
    ___#_
    ___R_
    ___A_
    #ANT#
    ___#_
    ___#__
    _#ART#
    ___A__
    #ANT#_
    ___#__
    ___#___
    ___R___
    __#ART#
    #ANT#__
    ___#___
    ___#_
    ___R_
    _#_A_
    #ANT#
    _R_#_
    _T___
    _#___
    '''
    crosswords = [Crossword2()]
    crosswords[0].embed((0, 0), HORIZONTAL, words[0])
    while True:
        if not crosswords: break
        crosswords = sorted(crosswords, cmp=lambda c1, c2: cmp(evaluate_crossword(c1), evaluate_crossword(c2)))
        base = crosswords.pop(0)
        if monitor:
            print '%d candidates...'%(len(crosswords))
            if isinstance(monitor, dict):
                base.dump(empty=monitor['EMPTY'], filled=monitor['FILLED'])
            else:
                base.dump()
            print
        try:
            candidates = generate_candidates(words, base)
            yield base
            crosswords += candidates
        except ValueError:
            # discard this base
            pass


def generate_candidates(words, base):
    sequences = base.all_disconnected_sequences()
    fit_words = []
    for sequence in sequences:
        fit_words_for_seq = [(p, d, w) for (p, d, w) in propose_words(sequence, [w for w in words if w not in base.used_words]) if base.is_fit(p, d, w)]
        _, _, s = sequence
        if s.find('.') == -1 and len(s) > 1 and not fit_words_for_seq:
            # dead end; discard this base
            raise ValueError('no candidates found')
        fit_words += fit_words_for_seq
    candidates = []
    for p, d, w in fit_words:
        copy = base.copy()
        copy.embed(p, d, w)
        candidates.append(copy)
    return candidates


def propose_words(sequence, words):
    (p, d, seq) = sequence
    proposed_words = []
    for word in words:
        idx = 0
        while True:
            m = re.search(seq, word[idx:])
            if not m: break
            proposed_words.append((OpenGrid.pos_inc(p, -(m.start() + idx), d), d, word))
            idx += m.start() + 1
    return proposed_words


def evaluate_crossword(c):
    # return -len(c.used_words)
    return (c.grid.width + c.grid.height) * 1.0 / len(c.used_words) ** 2
    # return (c.grid.width * c.grid.height) * 1.0 / sum([len(w) for w in c.used_words])


def pickup_crosswords(words, dump_option=None, monitor=False):
    best = 9999
    for c in build_crossword2(words, monitor=monitor):
        if evaluate_crossword(c) < best:
            if dump_option:
                c.dump(empty=dump_option['EMPTY'], filled=dump_option['FILLED'])
            else:
                c.dump()
            best = evaluate_crossword(c)
            print 'score: %f'%(best)
            print


if __name__ == '__main__':
    import doctest
    doctest.testmod()
