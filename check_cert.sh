#!/bin/bash

if openssl x509 -checkend 86400 -noout -in /etc/letsencrypt/live/vm.rashidisayev.com/cert.pem
then
  echo "Certificate is good for another day!"
else
  curl -X POST "https://api.telegram.org/bot903089995:AAE2uS2_eVNyl3-oUeHovjI1Kan5-7hF5qo/sendMessage" -d "chat_id=-1001157819373&text=Certificate of vm.rashidisayev.com has expired or will do so within 24 hours! Please inform Rashid Isayev or Mohsen Dalil"

fi
