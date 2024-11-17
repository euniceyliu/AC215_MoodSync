FROM python:3.11-slim-bookworm

ARG DEBIAN_PACKAGES="build-essential git screen vim"

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV PYENV_SHELL=/bin/bash
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/llm-service-account.json
ENV PYTHONUNBUFFERED=1

# Create app user
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
    mkdir -p /app/.coverage-reports && \
    chown -R app:app /app && \
    chmod -R 777 /app

# Create a directory for python packages
RUN mkdir -p /home/app/.local && \
    chown -R app:app /home/app/.local

# Switch to the app user
USER app
WORKDIR /app

# Copy Pipfile and install dependencies
COPY --chown=app:app Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile

# Add the rest of the source code
COPY --chown=app:app . .

CMD ["/bin/bash"]