#!/bin/sh

ip=$(ip addr show | grep inet | grep ra0 | perl -nle'/(\d+\.\d+\.\d+\.\d+)/ && print $1' | head -n 1)
echo "$ip"
php -S $ip:8080 -t /var/log/spine/imaging
