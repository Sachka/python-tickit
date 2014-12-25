
from ctypes import c_int, byref
from functools import wraps
import io

from tickit.pen import Pen
from tickit._tickit import tickit

class Term:
    def __init__(self, **kwargs):
        self._ids = []
        self._handlers = []

        if 'termtype' in kwargs:
            self._term = tickit.term_new_for_termtype(bytes(kwargs['termtype'], 'ascii'))
        else:
            self._term = tickit.term_new()

        if 'utf8' not in kwargs:
            kwargs['utf8'] = True

        tickit.term_set_utf8(self._term, kwargs['utf8'])
        self._utf8 = kwargs['utf8']

        if 'writer' in kwargs:
            tickit.term_set_output_func(self._term, kwargs['writer'], None)

        if 'output_handle' in kwargs:
            handle = kwargs['output_handle']

            if isinstance(handle, io.IOBase):
                fd = handle.fileno()
            elif isinstance(handle, int):
                fd = handle
            else:
                raise TypeError('output handle must be file descriptor or IOBase subclass')

            tickit.term_set_output_fd(fd)

        if 'input_handle' in kwargs:
            handle = kwargs['input_handle']

            if isinstance(handle, io.IOBase):
                fd = handle.fileno()
            elif isinstance(handle, int):
                fd = handle
            else:
                raise TypeError('input handle must be file descriptor or IOBase subclass')

            tickit.term_set_input_fd(fd)

    @classmethod
    def new_for_termtype(cls, term, **kwargs):
        kwargs['termtype'] = term
        return cls(**kwargs)

    def get_input_handle(self):
        return tickit.tickit_term_get_input_handle(self._term)

    def get_output_handle(self):
        return tickit.tickit_term_get_output_handle(self._term)

    @property
    def input_handle(self):
        return self.get_input_handle()

    @property
    def output_handle(self):
        return self.get_output_handle()

    def set_output_buffer(self, size):
        tickit.term_set_output_buffer(self._term, size)

    def await_started(self, msec):
        tickit.term_await_started(self._term, msec)

    def flush(self):
        tickit.term_flush(self._term)

    def bind_event(self, event, func, data):
        func = tickit.TermEventFunc(func)

        id = tickit.term_bind_event(event, func, data)
        self._ids.append(id)
        self._handlers.append(func)

        return id

    def unbind_event_id(self, id):
        if id not in self._ids:
            raise KeyError('no handler for id')

        idx = self._ids.index(id)
        self._ids.pop(idx)
        self._handlers.pop(idx)

    def refresh_size(self):
        tickit.term_refresh_size(self._term)

    def set_size(self, lines, cols):
        tickit.term_set_size(self._term, lines, cols)

    @property
    def lines(self):
        lines = c_int()
        cols  = c_int()

        tickit.term_get_size(self._term, byref(lines), byref(cols))

        return lines

    @property
    def cols(self):
        lines = c_int()
        cols  = c_int()

        tickit.term_get_size(self._term, byref(lines), byref(cols))

        return cols

    def goto(self, line, col):
        return tickit.term_goto(self._term, line, col)

    def move(self, line, col):
        tickit.term_move(self._term, line, col)

    def scrollrect(self, top, left, lines, cols, down, right):
        return tickit.term_scrollrect(self._term, top, left, lines, cols, down, right)

    def chpen(self, pen=None, **kwargs):
        if pen is None:
            pen = Pen(**kwargs)

        tickit.term_chpen(self._term, pen._pen)

    def setpen(self, pen=None, **kwargs):
        if pen is None:
            pen = Pen(**kwargs)

        tickit.term_setpen(self._term, pen._pen)

    def print(self, text, pen=None):
        if pen is not None:
            self.setpen(pen)

        tickit.term_print(self._term, bytes(text, 'UTF-8' if self._utf8 else 'ascii'))

    def clear(self, pen=None):
        if pen is not None:
            self.setpen(pen)

        tickit.term_clear(self._term)

    def erasech(self, count, moveend, pen=None):
        if pen is not None:
            self.setpen(pen)

        tickit.term_erasech(count, moveend)

    def getctl_int(self, control):
        return tickit.term_getctl_int(self._term, control)

    def setctl_int(self, control, value):
        return tickit.term_setctl_int(self._term, control, value)

    def setctl_str(self, control, value):
        return tickit.term_setctl_str(self._term, control, bytes(value, 'ascii'))

    def input_push_bytes(self, data):
        tickit.term_input_push_bytes(self._termm, bytes(data, 'ascii'))

    def input_readable(self):
        tickit.term_input_readable(self._term)

    def input_wait(self, timeout):
        tickit.term_input_wait(self._term, timeout)

    def check_timeout(self):
        return tickit.term_check_timeout(self._term)

TermControl = tickit.TermControl

__all__ = ['Term', 'TermControl']
