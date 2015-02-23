# encoding: utf-8

words = [
    u'りんご',
    u'みかん',
    u'ごりら',
    u'らくご'
]


class OpenGrid(object):

    FILLED = u'凸'
    EMPTY = u'＿'
    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self):
        self.cells = {}

    def copy(self):
        copied = OpenGrid()
        copied.cells = self.cells.copy()
        return copied

    def set(self, pos, value):
        assert self.get(pos) == value or pos not in self.cells
        if value == Grid.EMPTY: return
        self.cells[pos] = value

    def get(self, pos):
        if pos in self.cells:
            return self.cells[pos]
        return Grid.EMPTY

    @staticmethod
    def pos_inc(pos, increment, direction):
        row, col = pos
        return (row + (increment if direction == Grid.VERTICAL else 0),
                col + (increment if direction == Grid.HORIZONTAL else 0))

    def poslist(self, pos, length, direction):
        return [Grid.pos_inc(pos, i, direction) for i in range(length)]

    def is_empty(self, pos):
        return self.get(pos) == Grid.EMPTY

    def get_word(self, pos, direction, length):
        return u''.join([self.get(p) for p in self.poslist(pos, length, direction)])


class Grid(OpenGrid):

    u'''
    >>> grid = Grid(3, 3)
    >>> grid.dump()
    凸凸凸凸凸
    凸＿＿＿凸
    凸＿＿＿凸
    凸＿＿＿凸
    凸凸凸凸凸
    >>>
    '''

    def __init__(self, width, height):
        super(Grid, self).__init__()
        self.colmin = -1
        self.colmax = width
        self.rowmin = -1
        self.rowmax = height
        self.fill_wall()

    def copy(self):
        copied = Grid(self.colmax, self.rowmax)
        copied.cells = self.cells.copy()
        return copied

    def fill_wall(self):
        self.set((self.rowmin, self.colmin), Grid.FILLED)
        self.set((self.rowmax, self.colmin), Grid.FILLED)
        self.set((self.rowmin, self.colmax), Grid.FILLED)
        self.set((self.rowmax, self.colmax), Grid.FILLED)
        for row in range(self.rowmin + 1, self.rowmax):
            self.set((row, self.colmin), Grid.FILLED)
            self.set((row, self.colmax), Grid.FILLED)
        for col in range(self.colmin + 1, self.colmax):
            self.set((self.rowmin, col), Grid.FILLED)
            self.set((self.rowmax, col), Grid.FILLED)

    def get(self, pos):
        (r, c) = pos
        if (r < self.rowmin or self.rowmax < r or
           c < self.colmin or self.colmax < c):
            return Grid.EMPTY
        return super(Grid, self).get(pos)

    def dump(self):
        lines = u''
        for row in range(self.rowmin, self.rowmax + 1):
            if lines: lines += '\n'
            for col in range(self.colmin, self.colmax + 1):
                lines += self.get((row, col))
        print lines

    def allpos(self):
        return ((r, c)
                for r in range(self.rowmin, self.rowmax + 1)
                for c in range(self.colmin, self.colmax + 1))

    def get_col(self, col):
        return self.get_word((self.rowmin, col), Grid.VERTICAL, self.height)

    def get_row(self, row):
        return self.get_word((row, self.colmin), Grid.HORIZONTAL, self.width)

    def get_width(self):
        return self.colmax - self.colmin + 1
    width = property(get_width)

    def get_height(self):
        return self.rowmax - self.rowmin + 1
    height = property(get_height)

    def fill_all_empty(self):
        for pos in self.allpos():
            if self.get(pos) == Grid.EMPTY:
                self.set(pos, Grid.FILLED)

    def shrink(self):
        u'''
        >>> g = Grid(3, 3)
        >>> g.fill_all_empty()
        >>> g.shrink()
        >>> g.dump()
        凸
        >>> g = Grid(3, 3)
        >>> g.set((1, 1), u'ぬ')
        >>> g.fill_all_empty()
        >>> g.shrink()
        >>> g.dump()
        凸凸凸
        凸ぬ凸
        凸凸凸
        '''
        self.shrink_right()
        self.shrink_left()
        self.shrink_top()
        self.shrink_bottom()

    def shrink_right(self):
        while True:
            if (Grid.FILLED * self.height ==
               self.get_col(self.colmin) ==
               self.get_col(self.colmin + 1)):
                self.colmin += 1
            else:
                break

    def shrink_left(self):
        while True:
            if (Grid.FILLED * self.height ==
               self.get_col(self.colmax) ==
               self.get_col(self.colmax - 1)):
                self.colmax -= 1
            else:
                break

    def shrink_top(self):
        while True:
            if (Grid.FILLED * self.width ==
               self.get_row(self.rowmin) ==
               self.get_row(self.rowmin + 1)):
                self.rowmin += 1
            else:
                break

    def shrink_bottom(self):
        while True:
            if (Grid.FILLED * self.width ==
               self.get_row(self.rowmax) ==
               self.get_row(self.rowmax - 1)):
                self.rowmax -= 1
            else:
                break


class Crossword(object):

    def __init__(self, width, height):
        self.grid = Grid(width, height)
        self.connected = {}

    def allpos(self):
        return self.grid.allpos()

    def dump(self):
        return self.grid.dump()

    def copy(self):
        copied = Crossword(self.grid.width, self.grid.height)
        copied.grid = self.grid.copy()
        copied.connected = self.connected.copy()
        return copied

    def get(self, pos):
        return self.grid.get(pos)

    def is_empty(self, pos):
        return self.grid.is_empty(pos)

    def is_embedded(self, pos):
        return not(self.is_empty(pos) or self.get(pos) == Grid.FILLED)

    def is_connected(self, pos1, pos2):
        return (pos1, pos2) in self.connected

    def connect(self, pos1, pos2):
        self.connected[(pos1, pos2)] = True

    def is_fit(self, pos, direction, word):
        u'''
        >>> c = Crossword(3, 3)
        >>> c.is_fit((0, 0), Grid.HORIZONTAL, u'りんご')
        True
        >>> c.grid.set((0, 0), u'り')
        >>> c.is_fit((0, 0), Grid.VERTICAL, u'りんご')
        True
        >>> c.grid.set((2, 0), u'ぬ')
        >>> c.is_fit((0, 0), Grid.HORIZONTAL, u'りんご')
        True
        >>> c.is_fit((0, 0), Grid.VERTICAL, u'りんご')
        False
        >>> c.grid.set((1, 1), u'ぬ')
        >>> c.is_fit((1, 0), Grid.HORIZONTAL, u'りんご')
        False

        単語内に単語を重ねない
        >>> c = Crossword(3, 3)
        >>> c.embed((0, 0), Grid.HORIZONTAL, u'みかん')
        >>> c.is_fit((0, 1), Grid.HORIZONTAL, u'かん')
        False

        前後は空白か埋まっている
        >>> c = Crossword(3, 3)
        >>> c.embed((0, 0), Grid.HORIZONTAL, u'みかん')
        >>> c.is_fit((1, 0), Grid.VERTICAL, u'かん')
        False
        '''
        if self.is_embedded(Grid.pos_inc(pos, -1, direction)):
            return False
        if self.is_embedded(Grid.pos_inc(pos, len(word), direction)):
            return False
        old_p = None
        for i, p in enumerate(self.grid.poslist(pos, len(word), direction)):
            if not self.is_empty(p) and word[i] != self.get(p):
                return False
            if i > 0:
                if self.is_connected(old_p, p):
                    return False
            old_p = p
        return True

    def embed(self, pos, direction, word):
        u'''
        単語の前後は埋められる
        >>> c = Crossword(5, 5)
        >>> c.embed((1, 1), Grid.HORIZONTAL, u'だんご')
        >>> c.embed((1, 1), Grid.VERTICAL, u'だるま')
        >>> c.dump()
        凸凸凸凸凸凸凸
        凸＿凸＿＿＿凸
        凸凸だんご凸凸
        凸＿る＿＿＿凸
        凸＿ま＿＿＿凸
        凸＿凸＿＿＿凸
        凸凸凸凸凸凸凸
        '''
        old_p = None
        for i, p in enumerate(self.grid.poslist(pos, len(word), direction)):
            self.grid.set(p, word[i])
            if i > 0:
                self.connect(old_p, p)
            old_p = p
        self.grid.set(Grid.pos_inc(pos, -1, direction), Grid.FILLED)
        self.grid.set(Grid.pos_inc(pos, len(word), direction), Grid.FILLED)

    def is_all_words_valid(self):
        for pos in self.allpos():
            if not self.is_embedded(pos):
                continue
            p1 = Grid.pos_inc(pos, 1, Grid.VERTICAL)
            if self.is_embedded(p1) and not self.is_connected(pos, p1):
                return False
            p2 = Grid.pos_inc(pos, 1, Grid.HORIZONTAL)
            if self.is_embedded(p2) and not self.is_connected(pos, p2):
                return False
        return True

    def finalize(self):
        self.grid.fill_all_empty()
        self.grid.shrink()
        self.normalize()

    def normalize(self):
        pass


def build_crossword(width, height, words, monitor=False):
    u'''
    >>> result = build_crossword(3, 2, [u'まめ', u'ごまめ'])
    >>> for r in result: r.dump()
    凸凸凸
    凸ま凸
    凸め凸
    凸凸凸
    凸凸凸凸凸
    凸ごまめ凸
    凸凸め凸凸
    凸凸凸凸凸
    凸凸凸凸凸
    凸凸凸ま凸
    凸ごまめ凸
    凸凸凸凸凸
    >>> result = build_crossword(3, 3, [u'りんご', u'だんご'])
    >>> for r in result: r.dump()
    凸凸凸凸凸
    凸りんご凸
    凸凸凸凸凸
    凸だんご凸
    凸凸凸凸凸
    凸凸凸凸凸
    凸り凸だ凸
    凸ん凸ん凸
    凸ご凸ご凸
    凸凸凸凸凸
    凸凸凸凸凸
    凸凸り凸凸
    凸だんご凸
    凸凸ご凸凸
    凸凸凸凸凸
    凸凸凸凸凸
    凸だ凸り凸
    凸ん凸ん凸
    凸ご凸ご凸
    凸凸凸凸凸
    凸凸凸凸凸
    凸凸凸り凸
    凸凸凸ん凸
    凸だんご凸
    凸凸凸凸凸
    凸凸凸凸凸
    凸凸だ凸凸
    凸りんご凸
    凸凸ご凸凸
    凸凸凸凸凸
    凸凸凸凸凸
    凸だんご凸
    凸凸凸凸凸
    凸りんご凸
    凸凸凸凸凸
    凸凸凸凸凸
    凸凸凸だ凸
    凸凸凸ん凸
    凸りんご凸
    凸凸凸凸凸

    '''
    crosswords = [Crossword(width, height)]
    for word in words:
        new_grids = []
        for grid in crosswords:
            fits = find_all_fit(grid, word)
            if not fits:
                new_grids.append(grid)
                continue
            for (r, c, d) in fits:
                new_grid = grid.copy()
                new_grid.embed((r, c), d, word)
                new_grids.append(new_grid)
        crosswords = new_grids
        if monitor:
            for c in crosswords:
                c.dump()
                print

    validated_crosswords = [g for g in crosswords if g.is_all_words_valid()]
    for g in validated_crosswords: g.finalize()
    return validated_crosswords


def find_all_fit(crossword, word):
    u'''
    >>> c = Crossword(3, 3)
    >>> find_all_fit(c, u'りんご')
    [(0, 0, 2), (0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 2), (2, 0, 2)]
    >>> c.grid.set((1, 2), u'ぬ')
    >>> find_all_fit(c, u'りんご')
    [(0, 0, 2), (0, 0, 1), (0, 1, 1), (2, 0, 2)]
    '''
    results = []
    for (r, c) in crossword.allpos():
        if crossword.is_fit((r, c), Grid.HORIZONTAL, word):
            results.append((r, c, Grid.HORIZONTAL))
        if crossword.is_fit((r, c), Grid.VERTICAL, word):
            results.append((r, c, Grid.VERTICAL))
    return results


if __name__ == '__main__':
    import doctest
    doctest.testmod()
