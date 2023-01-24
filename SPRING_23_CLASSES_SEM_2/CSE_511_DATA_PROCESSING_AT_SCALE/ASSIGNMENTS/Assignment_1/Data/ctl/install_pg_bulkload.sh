#!/bin/bash

PG_TARGET=$1
apt-get install "postgresql-server-dev-$PG_TARGET"
apt-get install "build-essential" "git" "libpam0g-dev"
apt-get install "libedit-dev" "libselinux1-dev" "openssl" "libssl-dev"

ln -s "/usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2" "/usr/lib/x86_64-linux-gnu/libgssapi_krb5.so"

git clone "https://github.com/ossc-db/pg_bulkload.git" /opt/pg_bulkload

cd /opt/pg_bulkload
make clean
make
make install

ln -s /opt/pg_bulkload/bin/pg_bulkload /usr/local/sbin/pg_bulkload
sudo -u postgres psql postgres < /opt/pg_bulkload/lib/pg_bulkload--1.0.sql