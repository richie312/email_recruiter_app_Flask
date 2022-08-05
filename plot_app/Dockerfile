FROM python:3.7-slim-buster

WORKDIR .

COPY . .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5002

CMD ["python3","plot.py"]
