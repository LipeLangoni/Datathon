FROM python:3.11-slim

WORKDIR /app

COPY ./requirements/requirements.txt /app/requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

RUN pip install uv

RUN uv pip install --system --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src

WORKDIR /app/src

EXPOSE 80

ENTRYPOINT ["/app/entrypoint.sh"]