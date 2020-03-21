FROM ubuntu:bionic
WORKDIR /usr/src

RUN  apt-get update

ENV TZ=America/Vancouver
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y python3.6 python3-pip python3-venv python3-tk wget curl git npm nodejs
RUN pip3 install wheel pip setuptools virtualenv py-solc-x eth-brownie

WORKDIR /app
COPY . .

ENTRYPOINT /bin/bash
