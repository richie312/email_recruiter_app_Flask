FROM python:3.6-slim

WORKDIR .

COPY . .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python3","main.py"]
