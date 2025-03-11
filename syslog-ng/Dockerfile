FROM ubuntu:22.04

RUN apt-get update 
RUN apt-get -y install vim 
RUN apt-get -y install syslog-ng syslog-ng-mod-sql libdbi1 libdbi-dev libdbd-mysql default-libmysqlclient-dev
EXPOSE 514
COPY syslog-ng.conf /etc/syslog-ng/
COPY demo.sh entrypoint.sh
RUN chmod +x entrypoint.sh
RUN echo "SYSLOGNG_OPTS=\"--no-caps\"" >> /etc/default/syslog-ng
ENTRYPOINT ["/entrypoint.sh"]
