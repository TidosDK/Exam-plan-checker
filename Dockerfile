FROM python:3.12.11

WORKDIR /app

COPY main.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt
RUN mkdir Resources


ENTRYPOINT ["python3", "main.py"]
