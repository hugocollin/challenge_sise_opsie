FROM ubuntu:22.04

RUN apt update
RUN apt install -y nmap

CMD ["nmap","-sV","-T5","infra-chall-ipt"] 
