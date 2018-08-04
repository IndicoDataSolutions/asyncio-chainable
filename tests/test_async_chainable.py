import pytest

from asyncio_chainable import async_chainable, async_chainable_class


@pytest.mark.asyncio
async def test_simple_chain():
    class Number:
        def __init__(self, num: int = 0):
            self.num = num

        @async_chainable
        async def add(self, num: int):
            self.num += num
            return self

        @async_chainable
        async def subtract(self, num: int):
            self.num -= num
            return self

    assert (await Number().add(5).subtract(2)).num == 3


@pytest.mark.asyncio
async def test_class_chain():
    @async_chainable_class
    class Number:
        def __init__(self, num: int = 0):
            self.num = num

        async def add(self, num: int):
            self.num += num
            return self

        async def subtract(self, num: int):
            self.num -= num
            return self

    assert (await Number().add(5).subtract(2)).num == 3
