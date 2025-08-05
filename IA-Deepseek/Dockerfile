FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN python -m venv /opt/venv

RUN . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

ENV PORT=8000

EXPOSE ${PORT}

CMD ["sh", "-c", "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT}"]
