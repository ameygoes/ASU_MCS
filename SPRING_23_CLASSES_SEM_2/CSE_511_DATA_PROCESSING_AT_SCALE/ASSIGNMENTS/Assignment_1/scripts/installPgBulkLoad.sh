# STOP THE SERVICE BEFORE RUNNING ANYTHING
sudo service postgresql stop

# REMOVE MODULES 
sudo apt-get -y --purge remove postgresql libpq-dev libpq5 postgresql-client-common postgresql-common
sudo rm -rf /var/lib/postgresql
sudo apt-get update -qq

# INSTALL NECESSARY MODULES
sudo apt-get -y install bc libpam-dev libedit-dev bison flex zlib1g-dev zlib1g build-essential
cd /root

# CLONE POSTGRES INTO FOLDER
git clone https://github.com/postgres/postgres.git postgres-dev
cd postgres-dev

# INSTALL POSTGRES 14
git checkout -b REL_14_STABLE origin/REL_14_STABLE


# EXPORT SOME ENVIRONMENT VARIABLES
export PGVERSION=14
export POSTGRES_HOME=/root/postgresInstall
mkdir -p $POSTGRES_HOME

# CREATE BINARIES AND INSTALL PSQL AND OTHER MODULES - MUST BE IN POSTGRES-DEV FOLDER
./configure --prefix=$POSTGRES_HOME
make -j 30
make install

# DEFINE SOME OTHER VARIABLES AFTER BINARIES HAVE BEEN CREATED
echo 'export PATH=$PATH:$POSTGRES_HOME/bin' >> ~/.bashrc
export PATH=$PATH:$POSTGRES_HOME/bin
which psql
echo 'export PGDATA=/root/pg_data' >> ~/.bashrc
export PGDATA=/root/pg_data
mkdir -p $PGDATA

#INITIALIZE DATABASE
initdb --no-locale -D $PGDATA

# START THE  PSQL SERVICE
pg_ctl -D $PGDATA start


# CREATE FOLDER FOR PG_BULKLOAD
mkdir /root/pg_bulkload
cd pg_bulkload
git clone https://github.com/ossc-db/pg_bulkload.git pg_bulkload
cd pg_bulkload
make
make install