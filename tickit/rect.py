
from ctypes import byref

try:
    from collections.abc import Container
except ImportError:
    # Python 3.0-3.2
    from collections import Container

import tickit._tickit as tickit

class Rect(Container):
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if not isinstance(args[0], str):
                raise TypeError('not a string')

            self.parse(args[0])
        else:
            top  = kwargs['top']
            left = kwargs['left']

            self._rect = tickit.rect()

            if 'lines' in kwargs:
                lines = kwargs['lines']
                cols  = kwargs['cols']

                tickit.rect_init_sized(byref(self._rect), top, left, lines, cols)
            else:
                bottom = kwargs['bottom']
                right  = kwargs['right']

                tickit.rect_init_bounded(byref(self._rect), top, left, bottom, right)

    def parse(self, string):
        self._rect = tickit.rect()

        lt, rt = string.split('..', 1)

        left, top = lt[1:-1].split(',', 1)
        bottom, right = rt[1:-1].split(',', 1)

        tickit.rect_init_bounded(by_ref(self._rect), top, left, bottom, right)

    @property
    def top(self):
        return self._rect.top
    @top.setter
    def top(self, value):
        self._rect.top = value

    @property
    def left(self):
        return self._rect.left
    @left.setter
    def left(self, value):
        self._rect.left = value

    @property
    def lines(self):
        return self._rect.lines
    @lines.setter
    def lines(self, value):
        self._rect.lines = value

    @property
    def cols(self):
        return self._rect.cols
    @cols.setter
    def cols(self, value):
        self._rect.cols = value

    @property
    def right(self):
        return self.left + self.cols

    @property
    def bottom(self):
        return self.top + self.lines

    def add(self, other):
        rects = (tickit.rect * 3)()

        count = tickit.rect_add(rects, byref(self._rect), byref(other._rect))

        ret = []

        for rect in rects:
            ret.push(Rect(top=rect.top, left=rect.left, lines=rect.lines, cols=rect.cols))

        return ret

    def subtract(self, other):
        rects = (tickit.rect * 4)()

        count = tickit.rect_subtract(rects, byref(self._rect), byref(other._rect))

        ret = []

        for rect in rects:
            ret.push(Rect(top=rect.top, left=rect.left, lines=rect.lines, cols=rect.cols))

        return ret

    def intersect(self, other):
        rect = tickit.rect()

        if tickit.rect_intersect(rect, byref(self._rect), byref(other._rect)):
            return Rect(top=rect.top, left=rect.left, lines=rect.lines, cols=rect.cols)

        return None

    def intersects(self, other):
        return self.intersect(other) is not None

    def __contains__(self, other):
        return self.contains(other)

    def contains(self, other):
        return tickit.rect_contains(byref(self._rect), byref(other._rect))

    def translate(self, down, right):
        return Rect(top=self.top + down, left=self.left + right, lines=self.lines, cols=self.cols)

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)

    def equals(self, other):
        return (
            self.top   == other.top   and
            self.left  == other.left  and
            self.lines == other.lines and
            self.cols  == other.cols
        )

    def linerange(self, start=None, stop=None):
        if start is None or start < self.top:
            start = self.top
        if stop is None or stop > self.bottom:
            stop = self.bottom

        start = max(self.top, start)
        stop  = min(self.bottom, stop + 1)

        return list(range(start, stop))

__all__ = ['Rect']
