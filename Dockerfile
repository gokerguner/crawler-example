FROM python:3.6.9

EXPOSE 5000

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -vvv --no-cache-dir -r requirements.txt

COPY . /usr/src/app
