FROM python:3.9
WORKDIR /server
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./server /server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]