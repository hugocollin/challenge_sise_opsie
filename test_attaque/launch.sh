#!/bin/bash
#
sudo docker build -t attaquant .
sudo docker run -dit --network challenge_sise_opsie_infra_chall --name attaque attaquant
