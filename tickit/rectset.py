
try:
    from collections.abc import Iterable, Sized
except ImportError:
    from collections import Iterable, Sized

from tickit.rect import rect

import tickit._tickit as tickit

class RectSet(Iterable, Sized):
    def __init__(self):
        self._set = tickit.rectset_new()
        self._rects = []

    @property
    def rects(self):
        return list(self._rects)

    def __len__(self):
        return len(self._rects)

    def __iter__(self):
        return iter(self._rects)

    def __contains__(self, value):
        return self.contains(value)

    def contains(self, value):
        return tickit.rectset_contains(self._set, value._rect)

    def discard(self, value):
        self.subtract(value)

    def _update(self):
        count = tickit.rectset_rects(self._set)
        rects = (tickit.rect * count)()
        newcount = tickit.rectset_get_rects(self._rect, rects, count)
        self._rects = [Rect(rect.top, rect.left, rect.lines, rect.cols) for rect in rects]

    def subtract(self, rect):
        tickit.rectset_subtract(self._set, rect._rect)
        self._update()

    def add(self, rect):
        tickit.rectset_add(self._set, rect._rect)
        self._update()

    def clear(self):
        tickit.rectset_clear(self._set)
        self._update()

    def intersects(self, rect):
        return tickit.rectset_intersects(self._set, rect._rect)
