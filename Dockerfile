#FROM python:3.10-slim
#
#WORKDIR /app
#
#COPY . .
#
#ENV PYTHONPATH=/app
#
#RUN apt-get update && apt-get install -y postgresql-client && \
#    pip install --no-cache-dir -r requirements.txt
#
#CMD ["python", "src/app.py"]

FROM python:3.10-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y postgresql-client && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install python-dotenv  # <-- ADICIONADO

CMD ["python", "src/app.py"]
