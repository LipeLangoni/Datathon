FROM python:3.11-slim

WORKDIR /app

COPY ./requirements/requirements.txt /app/requirements.txt

RUN pip install uv

RUN uv pip install --system --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src

WORKDIR /app/src

RUN python3 train.py
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]