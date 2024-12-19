FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

ENV BOT_TOKEN=8182443228:AAGznPxs3-VV3LpeAcwKSHXKc8HvvPOqcqU

ENV POSTGRES_USER=mariawasnotfound

ENV POSTGRES_PASSWORD=0000

ENV POSTGRES_DB=afisha_db

COPY . /app

CMD ["python3", "bot.py"]
