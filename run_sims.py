'''Run a set of simulations
Edmund Tang 2021-05-01'''

import rw3d
import mysql.connector
import plotly.express as px
import pandas as pd
from timer import timer

cnx = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'password',
    database = '3d_Propulsive_Walk'
    )

vList = [0, 1, 2, 3, 5, 10]

for v in vList:
    for _ in range(9):
        simID = rw3d.RW_sim(4000, 1000, 10**-5, v, cnx)
        rw3d.calc_angles(simID,cnx)
        rw3d.calc_MSD(simID,cnx)

        
cnx.close()









