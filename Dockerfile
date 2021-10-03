FROM python:3.8

WORKDIR /src

COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt
COPY . /src/

CMD python3 /src/app.py
