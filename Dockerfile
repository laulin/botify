FROM ubuntu

RUN apt-get update -y && apt-get install -y python3 python3-pip redis
COPY dist/botify-1.0.tar.gz /tmp/botify-1.0.tar.gz
RUN pip3 install /tmp/botify-1.0.tar.gz
RUN pip3 install redis
COPY test/ /test