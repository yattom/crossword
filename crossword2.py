# coding: utf-8

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
        >>> c.embed((0, 0), VERTICAL, 'AXE')
        >>> c.embed((1, 2), HORIZONTAL, 'IT')
        >>> c.dump()
        _#____
        #ANT#_
        _X#IT#
        _E____
        _#____
        >>> c.all_disconnected_sequences()
        [((1, 0), 2, 'X'), ((2, 0), 2, 'E'), ((0, 1), 1, 'N'), ((0, 2), 1, 'TI'), ((1, 3), 1, 'T')]
        '''
        sequences = []
        for pos, direction, length in [((r, self.grid.colmin), HORIZONTAL, self.grid.width) for r in range(self.grid.rowmin, self.grid.rowmax + 1)] + [((self.grid.rowmin, c), VERTICAL, self.grid.height) for c in range(self.grid.colmin, self.grid.colmax + 1)]:
            line = self.grid.get_word(pos, direction, length)
            poslist = self.grid.poslist(pos, direction, length)
            seq = ''
            for (i, (c, p)) in enumerate(zip(line, poslist)):
                if c == EMPTY or c == FILLED:
                    if seq:
                        sequences.append((seq_start, seq_direction, seq))
                        seq = ''
                    continue
                if not seq:
                    seq_start = p
                    seq_direction = direction
                seq += c
                if self.is_connected(poslist[i - 1], p):
                    seq = ''
            if seq:
                sequences.append((seq_start, seq_direction, seq))
        return sequences


def build_crossword2(words, monitor=False):
    '''
    >>> ans = build_crossword2(['ANT', 'ART', 'RAT'])
    >>> for a in ans: a.dump()
    _#___
    #ANT#
    #RAT#
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
        sequences = base.all_disconnected_sequences()
        if all([len(w) < 2 for (p, d, w) in sequences]):
            # valid; not neccessarily good nor complete
            yield base
        for sequence in sequences:
            fit_words = [(p, d, w) for (p, d, w) in propose_words(sequence, [w for w in words if w not in base.used_words]) if base.is_fit(p, d, w)]
            if len(sequence[2]) > 1 and not fit_words:
                # dead end; discard this base
                break
            for p, d, w in fit_words:
                copy = base.copy()
                copy.embed(p, d, w)
                crosswords.append(copy)


def propose_words(sequence, words):
    (p, d, seq) = sequence
    proposed_words = []
    for word in words:
        idx = 0
        while word.find(seq, idx) >= 0:
            proposed_words.append((OpenGrid.pos_inc(p, -word.find(seq), d), d, word))
            idx = word.find(seq, idx) + 1
    return proposed_words


def evaluate_crossword(c):
    return (c.grid.width + c.grid.height) * 1.0 / len(c.used_words)


def pickup_crosswords(words):
    best = 9999
    for c in build_crossword2(words):
        if evaluate_crossword(c) < best:
            c.dump()
            best = evaluate_crossword(c)
            print 'score: %f'%(best)
            print


if __name__ == '__main__':
    import doctest
    doctest.testmod()
