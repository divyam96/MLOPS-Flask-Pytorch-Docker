FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

MAINTAINER Imad Toubal

WORKDIR /app

COPY './requirements.txt' .

# RUN apt-get install libgtk2.0-dev pkg-config -yqq 

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "app.py"]