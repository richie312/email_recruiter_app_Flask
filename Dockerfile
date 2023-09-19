FROM python:3.7-slim-buster

WORKDIR .

COPY . .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5004

CMD ["python3","main.py"]
