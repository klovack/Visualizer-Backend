FROM ubuntu:latest
MAINTAINER fikriansyah@mrizki.com

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

COPY requirements.txt /opt/visualizer/requirements.txt
WORKDIR /opt/visualizer
RUN pip3 install -r requirements.txt

COPY visualizer /opt/visualizer/visualizer/

RUN mkdir -p /var/log/gunicorn3

ENV PYTHONIOENCODING=utf-8
ENV PYTHONASYNCIODEBUG=1

CMD ["gunicorn3", "-b", "0.0.0.0:5000", "visualizer:create_app()", "--workers=5", "--error-logfile", "/var/log/gunicorn/error.log", "--access-logfile", "/var/log/gunicorn/access.log", "--capture-output", "--log-level", "debug"]