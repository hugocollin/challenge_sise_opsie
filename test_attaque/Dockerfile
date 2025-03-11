FROM ubuntu:22.04

RUN apt update
RUN apt install -y nmap

COPY ./script_command.sh /script_command.sh
COPY ./directory-list-2.3-medium.txt /directory-list-2.3-medium.txt
RUN chmod +x /script_command.sh

ENTRYPOINT ["/bin/bash"]
