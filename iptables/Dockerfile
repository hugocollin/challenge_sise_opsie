FROM ubuntu:22.04
RUN echo "tmp"
RUN apt update
RUN apt install -y iptables openssh-server apache2 telnetd vsftpd xinetd mariadb-server
RUN apt install -y ulogd2 gnupg vim
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
RUN apt install apt-transport-https
RUN echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-8.x.list
RUN apt update && apt install -y logstash
COPY ulogd.conf /etc/ulogd.conf
COPY logstash.conf /logstash.conf
COPY ./inetd.conf /etc/inetd.conf
COPY ./iptables_config /iptables_config
EXPOSE 22 
EXPOSE 80
EXPOSE 21
EXPOSE 20
EXPOSE 23
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
