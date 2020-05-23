FROM python:3.5.9-alpine3.11
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn","--workers=2 app:app"]