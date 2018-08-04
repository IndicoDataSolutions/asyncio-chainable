# asyncio-chainable

Making asyncio coroutines chainable

Built on: Python3 and Docker (alpine) and Poetry (Package Manager)<br>
Maintained by: Chris Lee [sihrc.c.lee@gmail.com]

## Getting Started

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
$ poetry run python3 -m asyncio-chainable.main
```
