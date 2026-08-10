# ─── Base: Ubuntu 22.04 with Python 3.11 ───────────────────────────────────
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ─── System dependencies ─────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    # PostgreSQL client (for pg_isready in entrypoint)
    postgresql-client \
    # PDF processing
    poppler-utils \
    # Misc
    curl \
    && rm -rf /var/lib/apt/lists/*

# Make python3.11 the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Upgrade pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# ─── App setup ───────────────────────────────────────────────────────────────
WORKDIR /app

# Install Python dependencies first (layer caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project
COPY . /app/

# Create static and media directories
RUN mkdir -p /app/static /app/media

# Copy & make entrypoint executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app/django/django_project

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
