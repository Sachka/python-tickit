
from collections import namedtuple

from ctypes import c_int, byref, create_string_buffer

import tickit._tickit as tickit

Cell = namedtuple('Cell', 'char linemask pen')

class RenderBuffer:
    def __init__(self, **kwargs):
        self._rb = tickit.renderbuffer_new(kwargs['lines'], kwargs['cols'])

    @property
    def lines(self):
        lines = c_int()
        cols  = c_int()

        tickit.renderbuffer_get_size(byref(self._rb), byref(lines), byref(cols))

        return lines

    @property
    def cols(self):
        lines = c_int()
        cols  = c_int()

        tickit.renderbuffer_get_size(byref(self._rb), byref(lines), byref(cols))

        return cols

    @property
    def line(self):
        if tickit.renderbuffer_has_cursorpos(byref(self._rb)):
            line = c_int()
            col  = c_int()

            tickit.renderbuffer_get_cursorpos(byref(self._rb), byref(line), byref(col))

            return line
        else:
            return None

    @property
    def col(self):
        if tickit.renderbuffer_has_cursorpos(byref(self._rb)):
            line = c_int()
            col  = c_int()

            tickit.renderbuffer_get_cursorpos(byref(self._rb), byref(line), byref(col))

            return col
        else:
            return None

    def save(self):
        tickit.renderbuffer_save(byref(self._rb))

    def savepen(self):
        tickit.renderbuffer_savepen(byref(self._rb))

    def restore(self):
        tickit.renderbuffer_restore(byref(self._rb))

    def clip(self, rect):
        tickit.renderbuffer_clip(byref(self._rb), byref(rect._rect))

    def mask(self, rect):
        tickit.renderbuffer_mask(byref(self._rb), byref(rect._rect))

    def translate(self, down, right):
        tickit.renderbuffer_translate(byref(self._rb), down, right)

    def reset(self):
        tickit.renderbuffer_reset(byref(self._rb))

    def clear(self, pen):
        tickit.renderbuffer_clear(byref(self._rb), byref(pen._pen))

    def goto(self, line, col):
        tickit.renderbuffer_goto(byref(self._rb), line, col)

    def setpen(self, pen):
        tickit.renderbuffer_setpen(byref(self._rb), byref(pen._pen))

    def skip_at(self, line, col, length):
        tickit.renderbuffer_skip_at(byref(self._rb), line, col, length)

    def skip(self, length):
        tickit.renderbuffer_skip(byref(self._rb), length)

    def skip_to(self, col):
        tickit.renderbuffer_skip_to(byref(self._rb), col)

    def text_at(self, line, col, text, pen):
        return tickit.renderbuffer_text_at(byref(self._rb), line, col, bytes(text, 'UTF-8'), byref(pen._pen))

    def text(self, text, pen):
        return tickit.renderbuffer_text(byref(self._rb), bytes(text, 'UTF-8'), byref(pen._pen))

    def erase_at(self, line, col, length, pen):
        tickit.renderbuffer_erase_at(byref(self._rb), line, col, lengh, byref(pen._pen))

    def erase(self, length, pen):
        tickit.renderbuffer_erase(byref(self._rb), length, byref(pen._pen))

    def erase_to(self, col, pen):
        tickit.renderbuffer_erase_to(byref(self._rb), col, byref(pen._pen))

    def erase_rect(self, rect, pen):
        tickit.renderbuffer_erase_rect(byref(self._rb), byref(rect._rect), byref(pen._pen))

    def hline_at(self, line, startcol, endcol, style, pen, caps=0):
        tickit.renderbuffer_hline_at(byref(self._rb), line, startcol, endcol, style, byref(pen._pen), caps)

    def vline_at(self, startline, endline, col, style, pen, caps=0):
        tickit.renderbuffer_vline_at(byref(self._rb), startline, endline, col, style, byref(pen._pen), caps)

    def linebox_at(self, startline, endline, startcol, endcol, style, pen):
        self.hline_at(startline, startcol, endcol, style, pen)
        self.hline_at(stopline, startcol, endcol, style, pen)

        self.vline_at(startline, endline, startcol, style, pen)
        self.vline_at(startline, endline, endcol, style, pen)

    def char_at(self, line, col, codepoint, pen):
        tickit.renderbuffer_char_at(byref(self._rb), line, col, codepoint, byref(pen._pen))

    def char(self, codepoint, pen):
        tickit.renderbuffer_char(byref(self._rb), codepoint, byref(pen._pen))

    def flush_to_term(self, term):
        tickit.renderbuffer_flush_to_term(byref(self._rb), byref(term._term))
