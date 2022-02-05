import mysql.connector
import rw3d
from timer import timer
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

cnx = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'password',
    database = '3d_Propulsive_Walk'
    )

cursor = cnx.cursor()

# filter parameters
propulsiveSpeed = 0
stepsPerObservation = 1000
obsLimit = 4000

# choose simulation IDs
cursor.execute(f"""SELECT `simID` FROM `experiments` WHERE
               (`propulsiveSpeed` = {propulsiveSpeed} AND `stepsPerObservation` = {stepsPerObservation})""")
simIDs = cursor.fetchall()
simIDs = [x for t in simIDs for x in t]

# pull trajectory data for given IDs
allResults = []
for simID in simIDs:
    cursor.execute(f"""SELECT `simID`, `obsNum`, `xpos`, `ypos`, `zpos`, `xori`, `yori`, `zori`
                   FROM `trajectories` WHERE (`simID` = {simID} AND `obsNum` <= {obsLimit})""")
    results = cursor.fetchall()
    for row in results:
        allResults.append(row)

df = pd.DataFrame([[ij for ij in i] for i in allResults]) # convert list (allResults) to data frame
df.rename(columns = {0:"Simulation ID", 1:"obsNum", 2:"rx", 3:"ry", 4:"rz", 5:"qx", 6:"qy", 7:"qz"}, inplace = True)

steps = [x for x in list(range(obsLimit+1)) if x % 8 == 0] # choose frames to skip when rendering

fig_pos = rw3d.plotTrajectory3D(df, steps, mode="position", fileName = "rw3d_position_scatterplot_v00.html")

fig_ori = rw3d.plotTrajectory3D(df, steps, mode="orientation", fileName = "rw3d_orientation_scatterplot_v00.html")

