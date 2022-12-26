FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --host=0.0.0.0 --port=8000
