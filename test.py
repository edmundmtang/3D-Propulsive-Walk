import rw3d
import mysql.connector

cnx = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'password',
    database = '3d_Propulsive_Walk'
    )

spd = 10 # speed of interest
fitLim = 1.5

cursor = cnx.cursor()

cursor.execute(f"SELECT `simID` FROM `experiments` WHERE `propulsiveSpeed` = {spd}")
simIDs = [i for t in cursor.fetchall() for i in t]

p0 = [1, 9, 1.5]

result = rw3d.msdFit2d(simIDs, p0, cnx, fitLim)

print(result.fit_report())

cnx.close()
