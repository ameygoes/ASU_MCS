export PGVERSION=14
export POSTGRES_HOME=/root/postgresInstall
echo 'export PATH=$PATH:$POSTGRES_HOME/bin' >> ~/.bashrc
export PATH=$PATH:$POSTGRES_HOME/bin
echo 'export PGDATA=/root/pg_data' >> ~/.bashrc
export PGDATA=/root/pg_data