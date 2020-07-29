#!/bin/bash

if true | openssl x509 -noout -dates -in /etc/letsencrypt/live/vm.rashidisayev.com/cert.pem 2>/dev/null | \
  openssl x509 -noout -checkend 0; then
  echo "Certificate is not expired"
else
  echo "Certificate is expired"
fi