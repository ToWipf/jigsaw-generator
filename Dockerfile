FROM ubuntu:22.04

RUN apt update && apt install python3-pip -y
RUN pip install numba numpy
COPY . /app
ENTRYPOINT [ "/app/main.py" ]

## build: docker build -t puz .
## start: docker run -v $(pwd)/out:/output/ -d puz