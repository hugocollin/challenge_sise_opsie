#!/bin/bash

sudo docker build -t image_ipt_infra_chall .
sudo docker run -it --name cont_ipt_infra_chall --cap-add NET_ADMIN --network=infra_chall --hostname infra-chall-ipt --privileged image_ipt_infra_chall

