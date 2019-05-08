
##############################
#                            #
# Created by: Daniel Aguirre #
# Date: 2019/02/22           #
#                            #
##############################

# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# USER´s VARIABLES
filename = "MyLogoGCode.gcode"
filename_robtargets = "MyLogoGCode_robtargets.txt"
filename_moveLs = "MyLogoGCode_moveLs.txt"
filename_numArrays = "MyLogoGCode_numArrays.txt"

G90 = True

# Program variables
positions = pd.DataFrame([[0.0,0.0,-10.0]], columns=["x","y","z"])
robtargets = []
moveLs = []
NumArrays = []

# Extract GCode command specific information
def parseCommand(command, G90):    
    global positions
    temp = command.split()

    if len(temp) == 0:
        temp = [";"]

    if temp[0]=="M106":
        x = positions.iloc[-1].x
        y = positions.iloc[-1].y
        z = 0.0      
        
        newPosition = pd.DataFrame([[x,y,z]], columns=["x","y","z"])
        positions = pd.concat([positions, newPosition])

    elif temp[0]=="M107":
        x = positions.iloc[-1].x
        y = positions.iloc[-1].y
        z = -10.0      
        
        newPosition = pd.DataFrame([[x,y,z]], columns=["x","y","z"])
        positions = pd.concat([positions, newPosition])
    
    if temp[0]=="G00" or temp[0]=="G01":
    
        x = 0.0
        y = 0.0
        z = 0.0
        dx = 0.0
        dy = 0.0
        dz = 0.0
        
        for comp in temp:
            if comp.startswith("X"):
                dx = float(comp[1:])
            if comp.startswith("Y"):
                dy = float(comp[1:])
            if comp.startswith("Z"):
                dz = float(comp[1:])

        if G90==True: #Use absolute coordinates
            x = dx
            y = dy
            z = dz
        else:
            x = positions.iloc[-1].x + dx
            y = positions.iloc[-1].y + dy
            z = positions.iloc[-1].z + dz       

        newPosition = pd.DataFrame([[x,y,z]], columns=["x","y","z"])
        positions = pd.concat([positions, newPosition])

# Writes the Robtarget points into a file
def writeRobtarget(i, position):
    x = position.x
    y = position.y
    z = position.z
    string1 = "CONST robtarget "
    string2 = "p" + str(i)
    string3 = ":= [[" + str(x) + "," + str(y) + "," + str(z) + "], [-1, 0, 0, 0], [-1, 0, 1, 0], [ 9E+9,9E+9, 9E9, 9E9, 9E9, 9E9]];"
    string4 = "\n"
    robtarget = string1 + string2 + string3 + string4
    robtargets.append(robtarget)

# Writes the GCode points into a file
def writeNumArray(i, position):
    x = position.x
    y = position.y
    z = position.z
    string3 = "[" + str(x) + "," + str(y) + "," + str(z) + "], "
    string4 = "\n"
    NumArray = string3 + string4
    NumArrays.append(NumArray)

# Writes the ABB move commands into a file
def writeMoveL(i):
    string1 = "moveL "
    string2 = "p" + str(i)
    string3 = ",v100, fine, toolPenExterno \WObj:=wobjBlackboardMovil;"
    string4 = "\n"
    moveL = string1 + string2 + string3 + string4
    moveLs.append(moveL)

def plotPath(proyection="2d"):    
    x = np.array(positions.x, dtype=pd.Series)
    y = np.array(positions.y, dtype=pd.Series)
    z = np.array(positions.z, dtype=pd.Series)

    x0 = np.array([1,])
    y0 = np.array([1,])
         
    fig = plt.figure()

    if (proyection == "3d"):
        ax = Axes3D(fig)
        ax.plot(x,y,z)

    else:
        ax = fig.add_subplot(111)
        ax.plot(x,y,"red")
        ax.scatter(x,y)

    plt.show()


################## MAIN ##################
print("Start")
# Load GCode and obtainn XYZ coordinates
file = open(filename,"r")
with open(filename,"r") as file:
    line = file.readline()
    lineNumberCount = 1
    while line:
        print("Line: " + str(lineNumberCount))
        line = file.readline()       
        parseCommand(line, G90)
        lineNumberCount += 1

# Write Robtargets and MoveL to a txt file
for i in range(0,positions.shape[0]-1):    
    position = positions.iloc[i]
    writeRobtarget(i, position)    
    writeMoveL(i)

with open(filename_robtargets,"w") as file:
    for line in robtargets:
        file.writelines(line)

with open(filename_moveLs,"w") as file:
    for line in moveLs:
        file.writelines(line)

with open(filename_numArrays,"w") as file:
    for line in NumArrays:
        file.writelines(line)

print("Conversion finished")
# Plot expected result
plotPath()



