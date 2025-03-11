#!/bin/bash

#!/bin/sh

iptables -F

# Démarre syslog-ng en arrière-plan
#syslog-ng -F &



service ssh start
service xinetd start
service apache2 start
service vsftpd start
service mariadb start
export PATH="/usr/share/logstash/bin/:$PATH"
logstash-plugin install logstash-output-syslog

iptables-restore < /iptables_config

ulogd -d  

logstash -f /logstash.conf &

tail -f /dev/null
