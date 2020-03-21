FROM python:3.8.2
RUN apt-get update -y
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
ENTRYPOINT ["python"]
CMD ["app.py"]