#!/bin/bash

if openssl x509 -checkend 86400 -noout -in /etc/letsencrypt/live/vm.rashidisayev.com/cert.pem
then
  echo "Certificate is good for another day!"
else
  echo "Certificate of vm.rashidisayev.com has expired or will do so within 24 hours!"
fi