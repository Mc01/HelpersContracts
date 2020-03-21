FROM python:3.8.2
RUN apt-get update -y
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
ENTRYPOINT ["python"]
CMD ["main.py"]