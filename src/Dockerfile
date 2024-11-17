FROM python:3.11-slim-bookworm

ARG DEBIAN_PACKAGES="build-essential git screen vim"

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

# Tell pipenv where the shell is
ENV PYENV_SHELL=/bin/bash

ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/llm-service-account.json

# Tell Python to disable buffering so we don't lose any logs
ENV PYTHONUNBUFFERED=1

# Create app user first so we get consistent UID/GID
RUN useradd -ms /bin/bash app -d /home/app -u 1000 -p "$(openssl passwd -1 Passw0rd)"

# Install system dependencies
RUN set -ex; \
    for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    mkdir -p /app && \
    mkdir -p /coverage && \
    chown -R app:app /app && \
    chown -R app:app /coverage && \
    chmod -R 777 /coverage

# Switch to the app user
USER app
WORKDIR /app

# Install python packages
COPY --chown=app:app src/Pipfile src/Pipfile.lock /app/

RUN pipenv sync

# Add the rest of the source code
COPY --chown=app:app . /app

CMD ["/bin/bash"]