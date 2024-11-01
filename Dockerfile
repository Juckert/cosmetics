FROM python:3.11
LABEL authors="30Team"

WORKDIR /tessfiles
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY tessfiles/ .


CMD ["python", "./run.py"]