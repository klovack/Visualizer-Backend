FROM ubuntu:18.04
MAINTAINER fikriansyah@mrizki.com

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

COPY requirements.txt /opt/visualizer/requirements.txt
WORKDIR /opt/visualizer
RUN pip3 install -r requirements.txt

COPY visualizer /opt/visualizer/visualizer/

CMD ["gunicorn3", "-b", "0.0.0.0:5000", "visualizer:create_app()", "--workers=5"]