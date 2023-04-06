FROM python:3.9-alpine

MAINTAINER Mukesh Baskaran <mukeshcse2015@gmail.com>

WORKDIR /app

COPY . /app

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

EXPOSE 8080

USER lbg_usr:lbg_usr

CMD ["/venv/bin/uvicorn","main:app","--host","0.0.0.0","--port","8080"]
