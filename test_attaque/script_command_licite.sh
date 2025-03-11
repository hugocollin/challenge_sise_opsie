#!/bin/bash

# Variables
TARGET="1nfra-chall-ipt"

while true; do
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

    # Connexion HTTPS (port 443)
    echo "Connexion HTTPS..."
    curl -I "https://$TARGET"

    # Connexion sur le port 8080
    echo "Connexion sur le port 8080..."
    curl -I "http://$TARGET:8080"

    # Connexion DNS (port 53)
    echo "Connexion DNS..."
    dig @$TARGET

    # Connexion SMTP (port 25)
    echo "Connexion SMTP..."
    (echo open "$TARGET" 25; sleep 1; echo quit) | telnet

    # Connexion IMAP (port 143)
    echo "Connexion IMAP..."
    (echo open "$TARGET" 143; sleep 1; echo quit) | telnet

    # Pause de 1 seconde avant la prochaine itération pour générer un maximum de logs
    sleep 1
done