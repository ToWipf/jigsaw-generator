FROM ubuntu:22.04

RUN apt update && apt install python3-pip -y
RUN pip install numba numpy
COPY . /app
ENTRYPOINT [ "/app/main.py" ]