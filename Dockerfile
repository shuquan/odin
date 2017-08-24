FROM ubuntu:16.04
MAINTAINER Shuquan Huang

RUN apt-get update && apt-get install -y --no-install-recommends \
                   gcc \
                   python-dev \
                   python-pip \
                   python3-pip \
                   vim

RUN pip install --upgrade pip && \
    pip install setuptools && \
    pip install python-redmine jupyter && \
    pip install pandas matplotlib && \
    pip install jieba pyLDAvis sklearn

RUN mkdir -p /opt/odin

COPY . /opt/odin

EXPOSE 8888

WORKDIR /opt/odin

RUN cp etc/msyh.ttf /usr/local/lib/python2.7/dist-packages/matplotlib/mpl-data/fonts/ttf/ && \
    cp etc/matplotlibrc /usr/local/lib/python2.7/dist-packages/matplotlib/mpl-data/matplotlibrc

CMD /usr/local/bin/jupyter notebook --ip=0.0.0.0 --allow-root --no-browser
