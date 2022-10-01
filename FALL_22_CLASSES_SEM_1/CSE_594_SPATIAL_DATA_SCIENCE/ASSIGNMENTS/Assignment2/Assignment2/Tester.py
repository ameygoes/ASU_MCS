#
# Tester
#
import os

import psycopg2
import sys
from sqlalchemy import create_engine
import Assignment2 as tasks

# TO DELETE BEFORE SUBMITTING
passw = '12345'
# passw = os.environ.get("POSTGRES_PASS")
DATABASE_NAME = 'space_assignment2'


# change the password to your postgres user password
def getEngineConnectionString(user='postgres', password=passw, dbname='postgres'):
    return "postgresql://" + user + ":" + password + "@localhost/" + dbname


# change the password to your postgres user password
def getOpenConnection(user='postgres', password=passw, dbname='postgres'):
    return psycopg2.connect(database=dbname, user=user, host='localhost', password=password)


def createDB(dbname='postgres'):
    """
    We create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getOpenConnection(dbname='postgres')
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute('SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname=\'%s\'' % (dbname,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('CREATE DATABASE %s' % (dbname,))  # Create the database
        print("DATABASE " + dbname + " created")

    # Clean up
    cur.close()
    con.commit()
    con.close()


if __name__ == '__main__':
    try:
        # Creating Database ddsassignment2
        print("Creating Database with desired name")
        createDB(DATABASE_NAME);

        print("Creating sqlalchemy engine")
        engine = create_engine(getEngineConnectionString(dbname=DATABASE_NAME))
        con = engine.connect()

        print("Creating postgis extension")
        try:
            # cur = con.cursor()
            con.execute("CREATE EXTENSION postgis;")  # Add PostGIS extension
        except:
            print("Unable to create postgis extension")
            pass

        print("Loading shape data")
        con.execute("drop table if exists shape_data")
        tasks.load_shape_data(engine, "inputs/airbnb/airbnb_Chicago 2015.shp")

        if con:
            con.close()

        # Getting psycopg2 connection to the database
        print("Getting psycopg2 connection to the created database")
        con = getOpenConnection(dbname=DATABASE_NAME)

        cur = con.cursor()
        cur.execute("Select ST_SRID(geometry) from shape_data limit 1")
        results = cur.fetchall()

        print("Loading point data and running spatial queries")
        cur = con.cursor()
        cur.execute("drop table if exists point_data")
        tasks.explore_spatial_sql(con, "inputs/abandoned_vehicles.csv", "outputs/query3.txt", "outputs/query4.txt",
                                  "outputs/query5.txt", "outputs/query6.txt", "outputs/query7.txt",
                                  "outputs/query8.txt", "outputs/query9.txt", "outputs/query10.txt")

        print("All queries successful")

        if con:
            con.close()

    except Exception as detail:
        print("Something bad has happened!!! This is the error ==> ", detail)

