
from ctypes import *
from enum import IntEnum
from functools import wraps

c_string = c_char_p

_lib = CDLL('libtickit.so')
_base = 'tickit'

__all__ = []

def function(name, restype, *argtypes):
    pkg_name = name
    name = '_'.join([_base, name])
    ret = getattr(_lib, name, None)

    if ret is None:
        raise KeyError('no such C function')

    ret.argtypes = argtypes
    ret.restype = restype

    globals()[pkg_name] = ret
    __all__.append(pkg_name)

def mkfunc(prefix, first=None):
    @wraps(function)
    def func(name, restype, *argtypes):
        if first is not None:
            argtypes = list(argtypes)
            argtypes.insert(0, first)

        name = '_'.join([prefix, name])
        function(name, restype, *argtypes)

    return func

class CEnum(IntEnum):
    @classmethod
    def from_param(cls, self):
        if not isinstance(self, cls):
            raise TypeError('invalid enum')
        return self

class Maybe(CEnum):
    unknown = -1
    false   = False
    true    = True

class EventType(CEnum):
    resize = 0x1
    key    = 0x2
    mouse  = 0x4
    change = 0x8
    unbind = 0x80000000

class KeyEventType(CEnum):
    key  = 1
    text = 2

class MouseEventType(CEnum):
    press   = 1
    drag    = 2
    release = 3
    wheel   = 4

class MouseWheel(CEnum):
    up   = 1
    down = 2

class Mod(CEnum):
    shift = 1
    alt   = 2
    ctrl  = 4

class Event(Structure):
    _fields_ = [
        ('lines',  c_int),
        ('cols',   c_int),
        ('str',    c_char_p),
        ('button', c_int),
        ('line',   c_int),
        ('col',    c_int),
        ('mod',    c_int),
    ]

class pen(Structure): pass

class PenAttribute(CEnum):
    foreground = 0
    background = 1
    bold       = 2
    underline  = 3
    italic     = 4
    reverse    = 5
    strike     = 6
    altfont    = 7
    blink      = 8

class PenAttribueType(CEnum):
    bool   = 0
    int    = 1
    colour = 2
    color  = 2 # for Americans

Pen_p = POINTER(pen)

_fpen = mkfunc('pen', Pen_p)

function('pen_new', Pen_p)
_fpen('clone', Pen_p)
_fpen('destroy', None)

_fpen('has_attr',        c_bool, PenAttribute)
_fpen('is_nonempty',     c_bool)
_fpen('nondefault_attr', c_bool, PenAttribute)
_fpen('is_nondefault',   c_bool)

_fpen('get_bool_attr', c_bool, PenAttribute)
_fpen('set_bool_attr', None, PenAttribute, c_bool)

_fpen('get_int_attr', c_int, PenAttribute)
_fpen('set_int_attr', None, PenAttribute, c_int)

_fpen('get_colour_attr', c_int, PenAttribute)
_fpen('set_colour_attr', None, PenAttribute, c_int)
_fpen('set_colour_attr_desc', None, PenAttribute, c_string)
# for Americans
pen_get_color_attr       = pen_get_colour_attr
pen_set_color_attr       = pen_set_colour_attr
pen_set_colour_attr_desc = pen_set_colour_attr_desc

_fpen('clear_attr', None, PenAttribute)
_fpen('clear', None)

_fpen('equiv_attr', c_bool, Pen_p, PenAttribute)
_fpen('equiv', c_bool, Pen_p)

_fpen('copy_attr', None, Pen_p, PenAttribute)
_fpen('copy', None, Pen_p, c_bool)

function('pen_attrtype', PenAttribueType, PenAttribute)
function('pen_attrname', c_string, PenAttribute)
function('pen_lookup_attr', PenAttribute, c_string)

class rect(Structure):
    _fields_ = [
        ('top', c_int),
        ('left', c_int),
        ('lines', c_int),
        ('cols', c_int)
    ]

Rect_p = POINTER(rect)

_frect = mkfunc('rect', Rect_p)
_frect('init_sized', None, c_int, c_int, c_int, c_int)
_frect('init_bounded', None, c_int, c_int, c_int, c_int)

_frect('intersect', c_bool, Rect_p, Rect_p)
_frect('intersects', c_bool, Rect_p)
_frect('contains', c_bool, Rect_p)

function('rect_add', c_int, rect * 3, Rect_p, Rect_p)
function('rect_subtract', c_int, rect * 4, Rect_p, Rect_p)

class rectset(Structure): pass

RectSet_p = POINTER(rectset)

_frectset = mkfunc('rectset', RectSet_p)
function('rectset_new', RectSet_p)
_frectset('destroy', None)
_frectset('clear',   None)

_frectset('rects',     c_size_t)
_frectset('get_rects', c_size_t, RectSet_p, c_size_t)

_frectset('add',      None, Rect_p)
_frectset('subtract', None, Rect_p)

_frectset('intersects', c_bool, Rect_p)
_frectset('contains',   c_bool, Rect_p)

class term(Structure): pass

Term_p = POINTER(term)

TermOutputFunc = CFUNCTYPE(None, Term_p, c_string, c_size_t, c_void_p)

_fterm = mkfunc('term', Term_p)
function('term_new', Term_p)
function('term_new_for_termtype', Term_p, c_string)
_fterm('destroy', None)
_fterm('get_termtype', c_string)

_fterm('set_output_fd', None, c_int)
_fterm('get_output_fd', c_int)
_fterm('set_output_func', None, TermOutputFunc, c_void_p)
_fterm('set_output_buffer', None, c_size_t)

_fterm('await_started_msec', None, c_long)
_fterm('flush', None)

_fterm('set_input_fd', None, c_int)
_fterm('get_input_fd', c_int)

_fterm('get_utf8', Maybe)
_fterm('set_utf8', None, c_bool)

_fterm('input_push_bytes', None, c_string, c_size_t)
_fterm('input_readable', None)
_fterm('input_check_timeout_msec', c_long)
_fterm('input_wait', None, c_long)

_fterm('get_size', None, POINTER(c_int), POINTER(c_int))
_fterm('set_size', None, c_int, c_int)
_fterm('refresh_size', None)

TermEventFunc = CFUNCTYPE(None, Term_p, EventType, Event, c_void_p)

_fterm('bind_event', c_int, EventType, TermEventFunc, c_void_p)
_fterm('unbind_event_id', None, c_int)

_fterm('print', None, c_string)
_fterm('printn', None, c_string, c_size_t)
_fterm('goto', c_bool, c_int, c_int)
_fterm('move', None, c_int, c_int)
_fterm('scrollrect', c_bool, c_int, c_int, c_int, c_int, c_int, c_int)

_fterm('chpen', None, Pen_p)
_fterm('setpen', None, Pen_p)

_fterm('clear', None)
_fterm('erasech', None, c_int, Maybe)

class TermControl(CEnum):
    altscreen      =  1
    cursorvis      =  2
    mouse          =  3
    cursorblink    =  4
    cursorshape    =  5
    icon_text      =  6
    title_text     =  7
    icontitle_text =  8
    keypad_app     =  9
    colors         = 10

class MouseMode(CEnum):
    off   = 0
    click = 1
    drag  = 2
    move  = 3

class CursorShape(CEnum):
    block    = 1
    under    = 2
    left_bar = 3

_fterm('getctl_int', c_bool, TermControl, POINTER(c_int))
_fterm('setctl_int', c_bool, TermControl, c_int)
_fterm('setctl_str', c_bool, TermControl, c_string)

function('string_seqlen', c_int, c_long)
function('string_putchar', c_size_t, c_string, c_size_t, c_long)

class stringpos(Structure):
    _fields_ = [
        ('bytes', c_size_t),
        ('codepoints', c_int),
        ('graphemes', c_int),
        ('columns', c_int),
    ]

StringPos_p = POINTER(stringpos)

function('string_count', c_size_t, c_string, StringPos_p, StringPos_p)
function('string_countmore', c_size_t, c_string, StringPos_p, StringPos_p)
function('string_ncount', c_size_t, c_string, c_size_t, StringPos_p, StringPos_p)
function('string_ncountmore', c_size_t, c_string, c_size_t, StringPos_p, StringPos_p)

function('string_mbswidth', c_int, c_string)
function('string_byte2col', c_int, c_string, c_size_t)
function('string_col2byte', c_size_t, c_string, c_int)

class renderbuffer(Structure): pass

RenderBuffer_p = POINTER(renderbuffer)

_frenderbuffer = mkfunc('renderbuffer', RenderBuffer_p)
function('renderbuffer_new', RenderBuffer_p, c_int, c_int)
_frenderbuffer('destroy', None)

_frenderbuffer('get_size', None, POINTER(c_int), POINTER(c_int))

_frenderbuffer('translate', None, c_int, c_int)
_frenderbuffer('clip', None, Rect_p)
_frenderbuffer('mask', None, Rect_p)

_frenderbuffer('has_cursorpos', c_bool)
_frenderbuffer('get_cursorpos', None, POINTER(c_int), POINTER(c_int))
_frenderbuffer('goto', None, c_int, c_int)
_frenderbuffer('ungoto', None)

_frenderbuffer('setpen', None, Pen_p)

_frenderbuffer('reset', None)
_frenderbuffer('save', None)
_frenderbuffer('savepen', None)
_frenderbuffer('restore', None)

_frenderbuffer('skip_at', None, c_int, c_int, c_int)
_frenderbuffer('skip', None, c_int)
_frenderbuffer('skip_to', None, c_int)
_frenderbuffer('text_at', c_int, c_int, c_int, c_string, Pen_p)
_frenderbuffer('text', c_int, c_string, Pen_p)
_frenderbuffer('erase_at', None, c_int, c_int, c_int, Pen_p)
_frenderbuffer('erase', None, c_int, Pen_p)
_frenderbuffer('erase_to', None, c_int, Pen_p)
_frenderbuffer('eraserect', None, Rect_p, Pen_p)
_frenderbuffer('clear', None, Pen_p)
_frenderbuffer('char_at', None, c_int, c_int, c_long, Pen_p)
_frenderbuffer('char', None, c_long, Pen_p)

class LineStyle(CEnum):
    single = 1
    double = 2
    thick  = 3

class LineCaps(CEnum):
    start = 1
    end   = 2
    both  = 3

_frenderbuffer('hline_at', None, c_int, c_int, c_int, LineStyle, Pen_p, LineCaps)
_frenderbuffer('vline_at', None, c_int, c_int, c_int, LineStyle, Pen_p, LineCaps)

_frenderbuffer('flush_to_term', None, Term_p)

class LineMask(Structure):
    _fields_ = [
        ('north', c_char),
        ('south', c_char),
        ('east', c_char),
        ('west', c_char),
    ]

_frenderbuffer('get_cell_active', c_int, c_int, c_int)
_frenderbuffer('get_cell_text', c_size_t, c_int, c_int, c_string, c_size_t)
_frenderbuffer('get_cell_linemask', LineMask, c_int, c_int)
_frenderbuffer('get_cell_pen', Pen_p, c_int, c_int)

class SpanInfo(Structure):
    _fields_ = [
        ('is_active', c_bool),
        ('n_columns', c_int),
        ('text', c_string),
        ('len', c_size_t),
        ('pen', Pen_p)
    ]

_frenderbuffer('get_span', c_size_t, c_int, c_int, SpanInfo, c_string, c_size_t)
