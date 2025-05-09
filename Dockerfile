FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y postgresql-client && \
    pip install --no-cache-dir -r requirements.txt

COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

CMD ["/wait-for-db.sh", "db", "5432", "python", "src/app.py"]