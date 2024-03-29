FROM python:3.7.4
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["flask","run", "--host=0.0.0.0"]
