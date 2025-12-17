"""
Making asyncio coroutines chainable

Author: Chris Lee
Email: sihrc.c.lee@gmail.com
"""

import inspect
from typing import Awaitable

RESERVED_ATTRS = ("__initial_coroutine__", "__chained_calls__", "__cached_result__")


class AsyncChainable:
    def __init__(self, initial_coroutine: Awaitable):
        self.__initial_coroutine__ = initial_coroutine
        self.__chained_calls__ = []
        self.__cached_result__ = None

    def __await__(self):
        async def chain():
            # If we have a cached result, use it instead of awaiting the initial coroutine
            if self.__cached_result__ is not None:
                chainable = self.__cached_result__
            else:
                chainable = await self.__initial_coroutine__
                # Cache the result after successful await
                self.__cached_result__ = chainable

            # Execute remaining chained calls
            for method, args, kwargs in self.__chained_calls__:
                chainable = await getattr(chainable, method)(*args, **kwargs)
                # Cache the result after each successful operation
                self.__cached_result__ = chainable

            # Clear the chain since all operations have been executed
            self.__chained_calls__.clear()
            return chainable

        return chain().__await__()

    def to_coroutine(self):
        """
        Convert this AsyncChainable to a coroutine object.
        This is useful for functions like asyncio.run_coroutine_threadsafe()
        that require a coroutine object rather than just an awaitable.
        """
        async def coro():
            return await self
        return coro()

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
