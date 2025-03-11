FROM ubuntu:22.04

RUN apt update
RUN apt install -y nmap openssh-client ftp curl telnet

COPY ./script_command.sh /script_command.sh
COPY ./script_command_licite.sh /script_command_licite.sh
COPY ./directory-list-2.3-medium.txt /directory-list-2.3-medium.txt
RUN chmod +x /script_command.sh
RUN chmod +x /script_command_licite.sh

ENTRYPOINT ["/bin/bash"]
