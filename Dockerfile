FROM python:3.8

LABEL author="Chris Lee"
LABEL email="sihrc.c.lee@gmail.com"

ARG EXTRAS="[test]"
ENV PATH=/asyncio-chainable/bin:/root/.poetry/bin:${PATH}

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

COPY . /asyncio-chainable
WORKDIR /asyncio-chainable

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD ["bash"]
