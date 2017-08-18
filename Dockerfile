FROM ubuntu:16.04
MAINTAINER Shuquan Huang

RUN apt-get update && apt-get install -y --no-install-recommends \
                   python-pip \
                   python-setuptools \
                   vim

RUN pip install python-redmine

RUN mkdir -p /opt/odin

COPY . /opt/odin

WORKDIR /opt
