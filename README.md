# asyncio-chainable

Making asyncio coroutines chainable

Built on: Python3 and Docker (alpine) and Poetry (Package Manager)<br>
Maintained by: Chris Lee [sihrc.c.lee@gmail.com]

## Example Usage
```python3
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
```

## Contributing: Getting Started

### Docker

- Additional Python3 dependencies can be added to requirements.txt<br>
- Tests are located in ./tests <br>
- To run the docker container with the basic requirements, dependencies, and the package installed:
  ```bash
  $ touch .env
  $ docker-compose up
  ```

### Poetry

```
$ poetry install
```
