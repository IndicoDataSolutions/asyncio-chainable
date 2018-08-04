"""
Making asyncio coroutines chainable

Author: Chris Lee
Email: sihrc.c.lee@gmail.com
"""
import inspect
from typing import Awaitable

RESERVED_ATTRS = ("__initial_coroutine__", "__chained_calls__")


class AsyncChainable:
    def __init__(self, initial_coroutine: Awaitable):
        self.__initial_coroutine__ = initial_coroutine
        self.__chained_calls__ = []

    def __await__(self):
        async def chain():
            chainable = await self.__initial_coroutine__
            for method, args, kwargs in self.__chained_calls__:
                chainable = await getattr(chainable, method)(*args, **kwargs)
            return chainable

        return chain().__await__()

    def __getattr__(self, attr, **getattr_kwargs):
        if attr in RESERVED_ATTRS:
            return super().__getattr__(self, attr, **getattr_kwargs)

        def tmp_callable(*args, **kwargs):
            self.__chained_calls__.append((attr, args, kwargs))
            return self

        return tmp_callable


def async_chainable(coroutine):
    def wrap_in_async_chainable(*args, **kwargs):
        return AsyncChainable(coroutine(*args, **kwargs))

    return wrap_in_async_chainable


def async_chainable_class(cls):
    for attr in dir(cls):
        method = getattr(cls, attr)
        if inspect.iscoroutinefunction(method):
            setattr(cls, attr, async_chainable(method))
    return cls
