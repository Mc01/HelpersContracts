FROM python:3.6.2

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
# for "with cache" usage
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN brownie compile

ENTRYPOINT /bin/bash
