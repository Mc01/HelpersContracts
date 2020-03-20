FROM python:latest

# Upgrade PIP
ENV PYTHONDONTWRITEBYTECODE=1
RUN pip install --upgrade pip

# Install Vyper
RUN git clone https://github.com/vyperlang/vyper.git /vyper
WORKDIR /vyper
RUN make
RUN vyper --version

# Install Ganache
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
RUN npm install npm@latest -g
RUN npm install -g ganache-cli

# Setup App
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN brownie compile

ENTRYPOINT /bin/bash
