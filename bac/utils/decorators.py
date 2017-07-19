from pathlib import Path
from enum import Enum

from bac.utils.pdb import PDBColumn
import warnings


class advanced_property(property):
    def __init__(self, *args, **kwargs):

        self._default = kwargs.get('default')
        self.type = kwargs.get('type')
        self.validator = kwargs.get('validator')
        self.warning_only = kwargs.get('warn', False)

        self.f = args[0] if args else None

        super(advanced_property, self).__init__(fget=self._fget, fset=self._fset)

    def __call__(self, f):
        self.f = f
        return self

    def _fget(self, obj):
        try:
            v = obj.__getattribute__(self.private_name)
        except AttributeError:
            v = None
        try:
            return v if v is not None else self.default(obj)
        except (AttributeError, TypeError):
            return None

    def _fset(self, obj, value):
        if value is None:
            obj.__setattr__(self.private_name, None)
        elif isinstance(value, self.type):
            value = self.type[0](value)
            if self.validator:
                if self.warning_only:
                    obj.__setattr__(self.private_name, value)
                    if not self.validator(value, obj):
                        warnings.warn("Setting {} to {} does not fulfill restrictions.".format(self.public_name, value), Warning)
                else:
                    if self.validator(value, obj):
                        obj.__setattr__(self.private_name, value)
                    else:
                        raise ValueError("Setting {} to {} does not fulfill restrictions.".format(self.public_name, value))
            else:
                obj.__setattr__(self.private_name, value)
        else:
            raise TypeError("{} must be of type {} instead of {}".format(self.public_name,
                                                                         ' or '.join(t.__name__ for t in self.type),
                                                                         type(value).__name__))

    @property
    def private_name(self):
        return "_{}".format(self.f.__name__)

    @property
    def public_name(self):
        return self.f.__name__

    def default(self, obj):
        if self._default is None: return None

        default_to_return = self._default(obj) if callable(self._default) else self._default

        return self.type[0](default_to_return)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, tuple):
            self._type = value
        else:
            if issubclass(value, Enum):
                self._type = (value, str)
            else:
                self._type = (value, )

    @property
    def validator(self):
        return self._validator

    @validator.setter
    def validator(self, value):
        if value is None:
            self._validator = None
            return

        new_validator = value
        argument_count = value.__code__.co_argcount if value.__code__.co_argcount > 0 else None
        self._validator = lambda *a: new_validator(*a[:argument_count])


class file(advanced_property):
    def __init__(self, *args, **kwargs):
        super(file, self).__init__(type=(Path, str), *args, **kwargs)


class column(advanced_property):
    def __init__(self, *args, **kwargs):
        super(column, self).__init__(type=PDBColumn, default=PDBColumn.O, *args, **kwargs)


class positive_decimal(advanced_property):
    def __init__(self, *args, **kwargs):
        super(positive_decimal, self).__init__(type=(float, int, str), validator=lambda x: x >= 0, *args, **kwargs)


class decimal(advanced_property):
    def __init__(self, *args, **kwargs):
        super(decimal, self).__init__(type=(float, int, str), *args, **kwargs)

class integer(advanced_property):
    def __init__(self, *args, **kwargs):
        super(integer, self).__init__(type=(int, str), *args, **kwargs)

class positive_integer(advanced_property):
    def __init__(self, *args, **kwargs):
        old_validator = kwargs.get('validator', lambda *y: True)
        kwargs['validator'] = lambda *x: old_validator(*x) and x[0] >= 0
        super(positive_integer, self).__init__(type=(int, str), *args, **kwargs)


class boolean(advanced_property):
    def __init__(self, *args, **kwargs):
        super(boolean, self).__init__(type=bool, *args, **kwargs)