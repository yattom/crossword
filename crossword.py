# encoding: utf-8

FILLED = '#'
EMPTY = '_'
VERTICAL = 1
HORIZONTAL = 2


class OpenGrid(object):

    def __init__(self):
        self.cells = {}
        self.stale = True

    def copy(self):
        copied = OpenGrid()
        copied.cells = self.cells.copy()
        copied.stale = True
        return copied

    def set(self, pos, value):
        assert self.get(pos) == value or pos not in self.cells
        if value == EMPTY: return
        self.cells[pos] = value
        self.stale = True

    def get(self, pos):
        if pos in self.cells:
            return self.cells[pos]
        return EMPTY

    @staticmethod
    def pos_inc(pos, increment, direction):
        row, col = pos
        return (row + (increment if direction == VERTICAL else 0),
                col + (increment if direction == HORIZONTAL else 0))

    def poslist(self, pos, length, direction):
        return [Grid.pos_inc(pos, i, direction) for i in range(length)]

    def is_empty(self, pos):
        return self.get(pos) == EMPTY

    def get_word(self, pos, direction, length):
        return ''.join([self.get(p) for p in self.poslist(pos, length, direction)])

    def refresh_covered_area(self):
        if not self.stale: return
        if not self.cells:
            self._colmin = self._colmax = self._rowmin = self._rowmax = 0
        else:
            self._colmin = min([c for (r, c) in self.cells.keys()])
            self._colmax = max([c for (r, c) in self.cells.keys()])
            self._rowmin = min([r for (r, c) in self.cells.keys()])
            self._rowmax = max([r for (r, c) in self.cells.keys()])
        self.stale = False

    def get_colmin(self):
        self.refresh_covered_area()
        return self._colmin
    colmin = property(get_colmin)

    def get_colmax(self):
        self.refresh_covered_area()
        return self._colmax
    colmax = property(get_colmax)

    def get_rowmin(self):
        self.refresh_covered_area()
        return self._rowmin
    rowmin = property(get_rowmin)

    def get_rowmax(self):
        self.refresh_covered_area()
        return self._rowmax
    rowmax = property(get_rowmax)

    def get_width(self):
        return self.colmax - self.colmin + 1
    width = property(get_width)

    def get_height(self):
        return self.rowmax - self.rowmin + 1
    height = property(get_height)

    def allpos(self):
        return ((r, c)
                for r in range(self.rowmin, self.rowmax + 1)
                for c in range(self.colmin, self.colmax + 1))

    def get_col(self, col):
        return self.get_word((self.rowmin, col), VERTICAL, self.height)

    def get_row(self, row):
        return self.get_word((row, self.colmin), HORIZONTAL, self.width)

    def delete_col(self, col):
        self.cells = dict(((r, c), self.cells[(r, c)])
                          for (r, c) in self.cells
                          if c != col)
        self.stale = True

    def delete_row(self, row):
        self.cells = dict(((r, c), self.cells[(r, c)])
                          for (r, c) in self.cells
                          if r != row)
        self.stale = True

    def fill_all_empty(self):
        for pos in self.allpos():
            if self.get(pos) == EMPTY:
                self.set(pos, FILLED)

    def dump(self, empty=None, filled=None):
        if not empty: empty = EMPTY
        if not filled: filled = FILLED
        lines = u''
        for row in range(self.rowmin, self.rowmax + 1):
            if lines: lines += '\n'
            for col in range(self.colmin, self.colmax + 1):
                v = self.get((row, col))
                if v == EMPTY: lines += empty
                elif v == FILLED: lines += filled
                else: lines += v
        print lines

    def shrink(self):
        u'''
        >>> g = Grid(3, 3)
        >>> g.fill_all_empty()
        >>> g.shrink()
        >>> g.dump()
        #
        >>> g = Grid(3, 3)
        >>> g.set((1, 1), 'X')
        >>> g.fill_all_empty()
        >>> g.shrink()
        >>> g.dump()
        ###
        #X#
        ###
        '''
        self.shrink_right()
        self.shrink_left()
        self.shrink_top()
        self.shrink_bottom()

    def shrink_right(self):
        while True:
            if (FILLED * self.height ==
               self.get_col(self.colmin) ==
               self.get_col(self.colmin + 1)):
                self.delete_col(self.colmin)
            elif (EMPTY * self.height ==
                  self.get_col(self.colmin)):
                self.delete_col(self.colmin)
            else:
                break

    def shrink_left(self):
        while True:
            if (FILLED * self.height ==
               self.get_col(self.colmax) ==
               self.get_col(self.colmax - 1)):
                self.delete_col(self.colmax)
            elif (EMPTY * self.height ==
                  self.get_col(self.colmax)):
                self.delete_col(self.colmax)
            else:
                break

    def shrink_top(self):
        while True:
            if (FILLED * self.width ==
               self.get_row(self.rowmin) ==
               self.get_row(self.rowmin + 1)):
                self.delete_row(self.rowmin)
            elif (EMPTY * self.width ==
                  self.get_row(self.rowmin)):
                self.delete_row(self.rowmin)
            else:
                break

    def shrink_bottom(self):
        while True:
            if (FILLED * self.width ==
               self.get_row(self.rowmax) ==
               self.get_row(self.rowmax - 1)):
                self.delete_row(self.rowmax)
            elif (EMPTY * self.width ==
                  self.get_row(self.rowmax)):
                self.delete_row(self.rowmax)
            else:
                break


class Grid(OpenGrid):

    u'''
    >>> grid = Grid(3, 3)
    >>> grid.dump()
    #####
    #___#
    #___#
    #___#
    #####
    >>>
    '''

    def __init__(self, width, height):
        super(Grid, self).__init__()
        colmin = -1
        colmax = width
        rowmin = -1
        rowmax = height
        self.fill_wall(rowmin, colmin, rowmax, colmax)

    def fill_wall(self, rowmin, colmin, rowmax, colmax):
        self.set((rowmin, colmin), FILLED)
        self.set((rowmax, colmin), FILLED)
        self.set((rowmin, colmax), FILLED)
        self.set((rowmax, colmax), FILLED)
        for row in range(rowmin + 1, rowmax):
            self.set((row, colmin), FILLED)
            self.set((row, colmax), FILLED)
        for col in range(colmin + 1, colmax):
            self.set((rowmin, col), FILLED)
            self.set((rowmax, col), FILLED)


class Crossword(object):

    def __init__(self, width, height):
        self.grid = Grid(width, height)
        self.connected = {}

    def allpos(self):
        return self.grid.allpos()

    def dump(self, *args, **argv):
        return self.grid.dump(*args, **argv)

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
        return not(self.is_empty(pos) or self.get(pos) == FILLED)

    def is_connected(self, pos1, pos2):
        return (pos1, pos2) in self.connected

    def connect(self, pos1, pos2):
        self.connected[(pos1, pos2)] = True

    def is_fit(self, pos, direction, word):
        u'''
        >>> c = Crossword(3, 3)
        >>> c.is_fit((0, 0), HORIZONTAL, 'ANT')
        True
        >>> c.grid.set((0, 0), u'A')
        >>> c.is_fit((0, 0), VERTICAL, 'ANT')
        True
        >>> c.grid.set((2, 0), u'X')
        >>> c.is_fit((0, 0), HORIZONTAL, u'ANT')
        True
        >>> c.is_fit((0, 0), VERTICAL, u'HUT')
        False
        >>> c.grid.set((1, 1), u'X')
        >>> c.is_fit((1, 0), HORIZONTAL, u'ANT')
        False

        単語内に単語を重ねない
        >>> c = Crossword(3, 3)
        >>> c.embed((0, 0), HORIZONTAL, u'BUS')
        >>> c.is_fit((0, 1), HORIZONTAL, u'US')
        False

        前後は空白か埋まっている
        >>> c = Crossword(3, 3)
        >>> c.embed((0, 0), HORIZONTAL, u'BUS')
        >>> c.is_fit((1, 0), VERTICAL, u'IN')
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
        >>> c.embed((1, 1), HORIZONTAL, u'ANT')
        >>> c.embed((1, 1), VERTICAL, u'ALL')
        >>> c.dump()
        #######
        #_#___#
        ##ANT##
        #_L___#
        #_L___#
        #_#___#
        #######
        '''
        old_p = None
        for i, p in enumerate(self.grid.poslist(pos, len(word), direction)):
            self.grid.set(p, word[i])
            if i > 0:
                self.connect(old_p, p)
            old_p = p
        self.grid.set(Grid.pos_inc(pos, -1, direction), FILLED)
        self.grid.set(Grid.pos_inc(pos, len(word), direction), FILLED)

    def is_all_words_valid(self):
        for pos in self.allpos():
            if not self.is_embedded(pos):
                continue
            p1 = Grid.pos_inc(pos, 1, VERTICAL)
            if self.is_embedded(p1) and not self.is_connected(pos, p1):
                return False
            p2 = Grid.pos_inc(pos, 1, HORIZONTAL)
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
    >>> result = build_crossword(3, 2, [u'AT', u'HAT'])
    >>> for r in result: r.dump()
    ###
    #A#
    #T#
    ###
    #####
    #HAT#
    ##T##
    #####
    #####
    ###A#
    #HAT#
    #####
    >>> result = build_crossword(3, 3, [u'GET', u'JET'])
    >>> for r in result: r.dump()
    #####
    #GET#
    #####
    #JET#
    #####
    #####
    #G#J#
    #E#E#
    #T#T#
    #####
    #####
    ##G##
    #JET#
    ##T##
    #####
    #####
    #J#G#
    #E#E#
    #T#T#
    #####
    #####
    ###G#
    ###E#
    #JET#
    #####
    #####
    ##J##
    #GET#
    ##T##
    #####
    #####
    #JET#
    #####
    #GET#
    #####
    #####
    ###J#
    ###E#
    #GET#
    #####

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
                c.dump(empty=monitor['EMPTY'], filled=monitor['FILLED'])
                print

    validated_crosswords = [g for g in crosswords if g.is_all_words_valid()]
    for g in validated_crosswords: g.finalize()
    return validated_crosswords


def find_all_fit(crossword, word):
    u'''
    >>> c = Crossword(3, 3)
    >>> find_all_fit(c, u'ART')
    [(0, 0, 2), (0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 2), (2, 0, 2)]
    >>> c.grid.set((1, 2), u'X')
    >>> find_all_fit(c, u'ART')
    [(0, 0, 2), (0, 0, 1), (0, 1, 1), (2, 0, 2)]
    '''
    results = []
    for (r, c) in crossword.allpos():
        if crossword.is_fit((r, c), HORIZONTAL, word):
            results.append((r, c, HORIZONTAL))
        if crossword.is_fit((r, c), VERTICAL, word):
            results.append((r, c, VERTICAL))
    return results


if __name__ == '__main__':
    import doctest
    doctest.testmod()
