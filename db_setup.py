'''Set up the database for propulsive particles
in 3D space

Edmund Tang 2021-05-01'''

import mysql.connector
from mysql.connector import errorcode

# Define tables
TABLES = {}
TABLES['experiments'] = (
    "CREATE TABLE `experiments` ("
    "`simID` INT AUTO_INCREMENT,"
    "`simDateTime` datetime DEFAULT NOW(),"
    "`simLen` INT NOT NULL,"
    "`stepSize` FLOAT NOT NULL,"
    "`propulsiveSpeed` FLOAT NOT NULL,"
    "`stepsPerObservation` INT NOT NULL,"
    "PRIMARY KEY (`simID`)"
    ") ENGINE = InnoDB")

TABLES['trajectories'] = (
    "CREATE TABLE `trajectories` ("
    "`entryID` INT AUTO_INCREMENT,"
    "`simID` INT NOT NULL,"
    "`obsNum` INT NOT NULL,"
    "`xpos` FLOAT NOT NULL,"
    "`ypos` FLOAT NOT NULL,"
    "`zpos` FLOAT NOT NULL,"
    "`xori` FLOAT NOT NULL,"
    "`yori` FLOAT NOT NULL,"
    "`zori` FLOAT NOT NULL,"
    "`theta` FLOAT,"
    "`psi` FLOAT,"
    "PRIMARY KEY (`entryID`),"
    "FOREIGN KEY (`simID`)"
    "   REFERENCES `experiments`(`simID`)"
    "   ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['MSDs'] = (
    "CREATE TABLE `MSDs` ("
    "`entryID` INT AUTO_INCREMENT,"
    "`simID` INT NOT NULL,"
    "`dt` FLOAT NOT NULL,"
    "`msd` FLOAT NOT NULL,"
    "`msd2d` FLOAT NOT NULL,"
    "`msad` FLOAT NOT NULL,"
    "PRIMARY KEY (`entryID`),"
    "FOREIGN KEY (`simID`)"
    "   REFERENCES `experiments`(`simID`)"
    "   ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['MSDfit'] = (
    "CREATE TABLE `MSDfit` ("
    "`setID` INT AUTO_INCREMENT,"
    "`setdDateTime` datetime DEFAULT NOW(),"
    "`fitLim` FLOAT NOT NULL,"
    "`fitD` FLOAT NOT NULL,"
    "`fitTau` FLOAT NOT NULL,"
    "`fitV` FLOAT NOT NULL,"
    "PRIMARY KEY (`setID`)"
    ") ENGINE=InnoDB")

TABLES['MSDfitset'] = (
    "CREATE TABLE `MSDfitset` ("
    "`setID` INT NOT NULL,"
    "`simID` INT NOT NULL,"
    "PRIMARY KEY (`setID`, `simID`),"
    "FOREIGN KEY (`setID`)"
    "   REFERENCES `MSDfit`(`setID`)"
    "   ON UPDATE CASCADE ON DELETE RESTRICT,"
    "FOREIGN KEY (`simID`)"
    "   REFERENCES `experiments`(`simID`)"
    "   ON UPDATE CASCADE ON DELETE RESTRICT"
    ") ENGINE=InnoDB")

# Connect to server
cnx = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'password'
    )
cursor = cnx.cursor()

# Ensure DB exists or create
DB_name = '3D_propulsive_walk'
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_name))
except mysql.connector.Error as err:
    print("Database {} does not exist.".format(DB_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_name))
        cnx.database = DB_name
    else:
        print(err)
        exit(1)        

# Attempt to create tables
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

#Wrap up
cnx.commit()
cursor.close()
cnx.close()
print("Database setup completed!")
