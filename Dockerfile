ARG REGISTRY_PATH='harbor.devops.indico.io/indico'
ARG BUILD_TAG=latest


# builder stage
FROM ${REGISTRY_PATH}/ubuntu-2204-build:${BUILD_TAG} as poetry-installer
ARG POETRY_INSTALL_ARGS
ARG GEMFURY_TOKEN

COPY pyproject.toml poetry.lock /venv/

RUN poetry export \
        -f requirements.txt \
        --output requirements.txt \
        --without-hashes  \
        ${POETRY_INSTALL_ARGS} && \
    sed -i "s/pypi.fury.io/${GEMFURY_TOKEN}@pypi.fury.io/" requirements.txt  && \
    pip3 install -r requirements.txt --no-deps


# image
FROM ${REGISTRY_PATH}/ubuntu-2204-deploy:${BUILD_TAG}
RUN apt-get update && \
    apt-get install \
      --no-install-recommends \
      --no-install-suggests \
      --yes \
      --fix-broken \
        libmagic1 && \
    apt-get clean

WORKDIR /asyncio_chainable

COPY --from=poetry-installer /venv /venv
COPY . /asyncio_chainable

CMD ["sleep", "infinity"]
