FROM python:3.11-slim

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# Install system build dependencies required to compile packages like psycopg2
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential \
		gcc \
		libpq-dev \
		libffi-dev \
		libssl-dev \
		cargo \
	&& rm -rf /var/lib/apt/lists/*

# Upgrade pip/setuptools/wheel to improve wheel availability
RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
