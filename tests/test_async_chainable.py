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


@pytest.mark.asyncio
async def test_chain_reawaitable():
    """Test that chains can be awaited multiple times and return the same result."""

    class Counter:
        def __init__(self, count: int = 0):
            self.count = count
            self.operation_count = 0

        @async_chainable
        async def increment(self, num: int = 1):
            self.count += num
            self.operation_count += 1
            return self

        @async_chainable
        async def double(self):
            self.count *= 2
            self.operation_count += 1
            return self

    # Create a chain
    chain = Counter().increment(5)

    # First await
    result1 = await chain
    assert result1.count == 5  # (0 + 5)
    assert result1.operation_count == 1  # increment + double

    # Second await - should use cached result, not re-execute operations
    result2 = await chain.double()
    assert result2.count == 10  # Same result
    assert result2.operation_count == 2  # Should still be 2, not 4

    # Verify it's the same object
    assert result1 is result2
