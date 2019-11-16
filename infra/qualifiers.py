"""
This module has not been tested extensively and should only
    be used for simple class hierarchies.
"""

import functools
import string
import random
import inspect

PRIVATE = []
FINAL = []


def _random_string():
    return ''.join(random.choices(string.ascii_letters, k=30))


def _caller_has_token(token):
    frame = inspect.stack()[0].frame
    count = 2
    while "self" not in frame.f_locals or count > 0:
        frame = frame.f_back
        if frame is None:
            return False
        if "self" in frame.f_locals:
            count -= 1
    return token in frame.f_locals["self"].__class__.__dict__


def _get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)


class Qualified(type):
    """
    Must be declared as the metaclass for any class that uses
        the qualifiers defined in this module
    """

    @staticmethod
    def __raise_private(base_cls, attr):
        def __do_raise(*args, **kwargs):
            raise AttributeError(f"Attribute {attr} is private "
                                 f"in class {base_cls.__qualname__}")

        return __do_raise

    @staticmethod
    def __raise_final(base_cls, attr):
        def __do_raise(*args, **kwargs):
            raise AttributeError(f"Attribute {attr} is final "
                                 f"in class {base_cls.__qualname__}")

        return __do_raise

    def __new__(mcs, cls, bases, dct):
        for base_cls in bases:
            for key in base_cls.__dict__:
                if f"{base_cls.__qualname__}.{key}" in PRIVATE and key not in dct:
                    dct[key] = Qualified.__raise_private(base_cls, key)
                if f"{base_cls.__qualname__}.{key}" in FINAL and key in dct:
                    Qualified.__raise_final(base_cls, key)()

        return super(Qualified, mcs).__new__(mcs, cls, bases, dct)


def private(func):
    """
    Qualify a method to be private
    """
    token = f"__{_random_string()}"
    PRIVATE.append(func.__qualname__)

    @functools.wraps(func)
    def __make_private(self, *args, **kwargs):
        setattr(self.__class__, token, 1)
        if not _caller_has_token(token):
            raise AttributeError(f"Attribute {func.__name__} is private "
                                 f"in class {self.__class__.__qualname__}")
        cached_class = self.__class__
        self.__class__ = _get_class_that_defined_method(func)
        _return = func.__get__(self, type(self))(*args, *kwargs)
        self.__class__ = cached_class
        return _return

    return __make_private


def protected(func):
    """
    Qualify a method to be protected
    """
    token = _random_string()

    @functools.wraps(func)
    def __make_protected(self, *args, **kwargs):
        setattr(self.__class__, token, 1)
        if not _caller_has_token(token):
            raise AttributeError(f"Attribute {func.__name__} is protected "
                                 f"in class {self.__class__.__qualname__}")
        cached_class = self.__class__
        self.__class__ = _get_class_that_defined_method(func)
        _return = func.__get__(self, type(self))(*args, *kwargs)
        self.__class__ = cached_class
        return _return

    return __make_protected


def public(func):
    """
    Qualify a method to be public
    """

    @functools.wraps(func)
    def __make_public(self, *args, **kwargs):
        cached_class = self.__class__
        self.__class__ = _get_class_that_defined_method(func)
        _return = func.__get__(self, type(self))(*args, *kwargs)
        self.__class__ = cached_class
        return _return

    return __make_public


def final(func):
    """
    Qualify a method to be final
    """
    FINAL.append(func.__qualname__)

    @functools.wraps(func)
    def __make_final(self, *args, **kwargs):
        cached_class = self.__class__
        self.__class__ = _get_class_that_defined_method(func)
        _return = func.__get__(self, type(self))(*args, *kwargs)
        self.__class__ = cached_class
        return _return

    return __make_final
