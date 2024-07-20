FROM python:3.7-slim-buster

WORKDIR .

COPY . .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
# make yagmail compatible with keyring inbuilt package of python.
RUN pip install --upgrade keyring importlib_metadata

EXPOSE 5001

CMD ["python3","main_without_auth.py"]
