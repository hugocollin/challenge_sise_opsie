#!/bin/bash

sudo docker build -t image_syslog_infra_chall .
sudo docker run -it --name cont_syslog_infra_chall --cap-add NET_ADMIN --network=infra_chall --ip=172.18.0.7 --hostname infra_chall_syslog --privileged image_syslog_infra_chall

