#!/usr/bin/env python
# coding: utf-8

# In[2]:


import psycopg2
import sys
from sqlalchemy import create_engine
import geopandas as gpd
import os

DATABASE_NAME = "lab_postgis"
PASSWORD =  os.environ.get("POSTGRES_PASS")


def getEngineConnectionString(user='postgres', password=PASSWORD, dbname='postgres'):
    return "postgresql://" + user + ":" + password + "@localhost/" + dbname


# In[5]:


def getOpenConnection(user='postgres', password=PASSWORD, dbname='postgres'):
    return psycopg2.connect(database = dbname, user = user, host='localhost', password= password)


# In[7]:


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
    else:
        print("Database with the given name already exists")

    # Clean up
    cur.close()
    con.commit()
    con.close()


# In[8]:


createDB(DATABASE_NAME)


# In[9]:


engine = create_engine(getEngineConnectionString(dbname = DATABASE_NAME))
con = engine.connect()
print("sqlalchemy engine created")


# In[10]:


try:
    con.execute("CREATE EXTENSION postgis;") # Add PostGIS extension
    print("postgis extension created")
except:
    print("Unable to create postgis extension")


# In[12]:


# def change_permissions_recursive(path, mode):
#     for root, dirs, files in os.walk(path, topdown=False):
#         for dir in [os.path.join(root,d) for d in dirs]:
#             os.chmod(dir, mode)
#     for file in [os.path.join(root, f) for f in files]:
#             os.chmod(file, mode)
#

# In[13]:


# change_permissions_recursive("C:\Amey\ASU\ASU_MCS\FALL_22_CLASSES_SEM_1\CSE_594_SPATIAL_DATA_SCIENCE\ASSIGNMENTS\lab_postgis\inputs", 0o777)


# In[14]:


dfAirbnb = gpd.read_file("C:\Amey\ASU\ASU_MCS\FALL_22_CLASSES_SEM_1\CSE_594_SPATIAL_DATA_SCIENCE\ASSIGNMENTS\lab_postgis\inputs")


# In[ ]:





# In[ ]:




