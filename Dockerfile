FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    make \
    texlive-base \
    texlive-bibtex-extra \
    texlive-fonts-recommended \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-luatex \
    dvipng \
    ghostscript \
  && rm -rf /var/lib/apt/lists/*

COPY requirements-gerby.txt /app/requirements-gerby.txt
RUN pip install --no-cache-dir -r requirements-gerby.txt

COPY . /app

RUN make gerby-deploy-build

CMD ["sh", "-lc", "cd gerby-website && gunicorn wsgi:application --bind 0.0.0.0:${PORT:-8080}"]
