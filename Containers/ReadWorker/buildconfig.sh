#!/bin/bash
set -e

# if $proxy_domain is not set, then default to $HOSTNAME
export hostloc=${hostloc:-$HOSTLOC}

/usr/local/bin/confd -onetime -backend env

echo "Starting Nginx"
exec /usr/sbin/nginx -c /etc/nginx/nginx.conf
