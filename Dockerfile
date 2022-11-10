# syntax=docker/dockerfile:1

FROM debian:latest as deb

WORKDIR /app

COPY .dockerignore .dockerignore

RUN apt-get update -y
RUN apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev cmake

RUN curl -O https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz
RUN tar -xvf Python-3.8.2.tar.xz
RUN cd Python-3.8.2 && ./configure --enable-optimizations
RUN cd Python-3.8.2 && make -j 4
RUN cd Python-3.8.2 && make altinstall
RUN python3.8 --version

RUN rm Python-3.8.2.tar.xz
RUN rm -r Python-3.8.2/

RUN python3.8 -m pip install --upgrade pip

RUN python3.8 -m pip install muon dash dash_daq dash_bootstrap_components leidenalg

COPY . .

RUN python3.8 -m pip install .

FROM scratch

COPY --from=deb / /

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app/guimov/"

CMD [ "guimov_launch", "-d", "datasets/datasets.txt", "-l", "logs/log"]
