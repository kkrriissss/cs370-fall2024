FROM python:3.9-slim


WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY test_mongodb.py /usr/src/app/
COPY test_qdrant.py /usr/src/app/
CMD ["tail", "-f", "/dev/null"]
