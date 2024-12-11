FROM python:3.11
LABEL authors="30Team"

WORKDIR /tessfiles

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY tessfiles/ .
COPY tessfiles/images/ .


CMD ["python", "run.py"]