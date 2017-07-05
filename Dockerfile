FROM ubuntu:16.04

RUN apt update && \
    apt install gimp -y

WORKDIR /root/.gimp-2.8/plug-ins
#COPY src/*.py ./

CMD /bin/bash
