#!/bin/bash
#This is auto updater of Lets encrypt certs for Proxmox vm.rashidisayev.com
#Shoud be run by crontab every 3 month
#Auth: Rashid Isayev rashid.isayev@adjust.com

systemctl stop ngnx
certbot certonly -d vm.rashidisayev.com
ovirt-shell <<EOF
1
EOF
sleep 5
rm -rf /etc/pve/local/pve-ssl.pem
rm -rf /etc/pve/local/pve-ssl.key
rm -rf /etc/pve/pve-root-ca.pem
cp /etc/letsencrypt/live/vm.rashidisayev.com/fullchain.pem  /etc/pve/local/pve-ssl.pem
cp /etc/letsencrypt/live/vm.rashidisayev.com/privkey.pem /etc/pve/local/pve-ssl.key
cp /etc/letsencrypt/live/vm.rashidisayev.com/chain.pem /etc/pve/pve-root-ca.pem
service pveproxy restart
service pvedaemon restart

systemctl start nginx