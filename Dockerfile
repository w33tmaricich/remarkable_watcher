FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./remarkable_watcher.py .

CMD ["python", "./remarkable_watcher.py"]
