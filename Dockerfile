FROM python:3.7-alpine

ENV PYTHONPATH "${PYTHONPATH}:."

ADD . /app
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]
