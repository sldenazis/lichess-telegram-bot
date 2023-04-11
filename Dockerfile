FROM python:3


RUN useradd -m -d /app app -s /bin/bash

USER app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data

COPY . .

ENV TOKEN=setme
ENV DB_PATH=/app/data/database.sqlite

CMD [ "python", "main.py" ]
