FROM python:3.10

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cinema_pon_backend.wsgi"]
