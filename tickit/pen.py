
import tickit._tickit as tickit

try:
    from collections.abc import Mapping, MutableMapping
except ImportError:
    # Python 3.0-3.2 maintained 2.7's location. :()
    from collections import Mapping, MutableMapping

def lookup_attr(name):
    name = bytes(name, 'ascii')
    attr = tickit.pen_lookup_attr(name)

    if attr == -1:
        raise KeyError('no such attribute')

_get = {
    tickit.PenAttributeType.color: tickit.pen_get_color_attr
    tickit.PenAttributeType.bool:  tickit.pen_get_bool_attr
    tickit.PenAttributeType.int:   tickit.pen_get_int_attr
}
_set = {
    tickit.PenAttributeType.color: tickit.pen_set_color_attr
    tickit.PenAttributeType.bool:  tickit.pen_set_bool_attr
    tickit.PenAttributeType.int:   tickit.pen_set_int_attr
}

class ImmutablePen(Mapping):
    def __init__(self, **kwargs):
        self._pen = tickit.pen_new()
        self._attrs = {}

        for k, v in kwargs:
            attr = lookup_attr(k)
            self._attrs[attr] = v
            func = _set[tickit.pen_attrtype(attr)]
            func(self._pen, attr, v)

    def _update(self):
        for attribute in PenAttribute:
            attr = self.getattr(attribute)
            name = tickit.pen_attrname(attribute)

            if attr == -1 or attr is False:
                continue
            else:
                self._attrs[name] = attr

    @classmethod
    def new_from_attrs(cls, **kwargs):
        return cls(**kwargs)

    def __len__(self):
        return len(self._attrs)

    def __iter__(self):
        return iter(self._attrs)

    def __contains__(self, name):
        return self.hasattr(name)

    def hasattr(self, name):
        attr = lookup_attr(name)
        return tickit.pen_has_attr(self._pen, attr)

    def mutable(self):
        return isinstance(self, MutablePen)

    def getattrs(self):
        return dict(self._attrs)

    def __getitem__(self, name):
        return self.getattr(name)

    def getattr(self, name):
        attr = lookup_attr(name)

        func = _get[tickit.pen_attrtype(attr)]

        return func(self._pen, attr)

    def equiv_attr(self, other, name):
        attr = lookup_attr(name)

        return tickit.pen_equiv_attr(self._pen, other._pen, attr)

    def __eq__(self, other):
        return self.equiv(other)

    def __ne__(self, other):
        return not self.equiv(other)

    def equiv(self, other):
        return tickit.pen_equiv(self._pen, other._pen)

    def clone(self):
        newbie = self.__class__()

        newbie._pen = tickit.pen_clone(self._pen)
        newbie._attrs = dict(self._attrs)

        return newbie

    def as_mutable(self):
        return MutablePen(**self._attrs)

    def as_immutable(self):
        return ImmutablePen(**self._attrs)

class MutablePen(ImmutablePen, MutableMapping)
    def setattrs(self, attrs):
        for k, v in attrs:
            self.setattr(k, v)

    def __setitem__(self, name, value):
        self.setattr(name, value)

    def setattr(self, name, value):
        attr = lookup_attr(name)

        func = _set[tickit.pen_attrtype(attr)]

        self._attrs[name] = value

        return func(self._pen, attr, value)

    def __delitem__(self, name):
        return self.delattr(name)

    def delattr(self, name):
        attr = lookup_attr(name)

        del self._attrs[attr]
        tickit.pen_clear_attr(self._pen, attr)

    def chattrs(self, attrs):
        for k, v in attrs:
            self.chattrs(k, v)

    def chattr(self, name, value):
        attr = lookup_attr(name)

        if value is not None:
            self.setattr(name, value)
        else:
            self.delattr(name)

Pen = MutablePen

PenAttributeType = PenAttributeType

__all__ = ['Pen', 'ImmutablePen', 'MutablePen', 'PenAttributeType']
