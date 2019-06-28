
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
import sys, getopt

# GLOBAL VARIABLES
inputfile = None
outputfile_robtargets = "outputfile_robtargets.txt"
outputfile_moveLs = "outputfile_moveLs.txt"

rotation = "[-1, 0, 0, 0]"
conf = "[-1, 0, 1, 0]"

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
    string3 = ":= [[" + str(x) + "," + str(y) + "," + str(z) + "], " + rotation + conf + ", [ 9E+9,9E+9, 9E9, 9E9, 9E9, 9E9]];"
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
def main(argv):

    global inputfile, outputfile_robtargets, outputfile_moveLs, rotation, conf

    try:
         opts, args = getopt.getopt(argv,"hi:o:r:c:",["help","ifile=","ofile="])
    except getopt.GetoptError:
         print('Error')
         sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage: GCode_to_Robtargets [-h | -i <inputfile> -o <outputfile>] ")
            print('Options and arguments:')
            print("-h     : Print this help message and exit")
            print("-i arg : Input the file to be converted into ABB instructions (also --ifile)")
            print("-o arg : Output filename containing the ABB instructions (also --ofile)")
            print("-r arg : Specify the rotation of the robtargets (also --rot). Default: [-1, 0, 0, 0]")
            print("-c arg : Specify the axis configuration of the robtargets (also --conf). Default: [-1, 0, 1, 0]")
            sys.exit()
            
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            
        elif opt in ("-o", "--ofile"):
            outputfile_robtargets = arg + "_robtargets.txt"
            outputfile_moveLs = arg + "_moveLs.txt"
            
        elif opt in ("-r", "--rot"):
            rotation = arg

        elif opt in ("-c", "--conf"):
            conf = arg


    # Check if Input file has been defined
    if inputfile == None:
         print("Inputfile not defined")
         sys.exit(2)
    
    # Load GCode and obtain XYZ coordinates
    file = open(inputfile,"r")
    with open(inputfile,"r") as file:
        line = file.readline()
        lineNumberCount = 1
        while line:
            print("Line: " + str(lineNumberCount))
            line = file.readline()       
            parseCommand(line, G90)
            lineNumberCount += 1
    
    # Write Robtargets and MoveL to a txt file
    for i in range(0, positions.shape[0]-1):    
        position = positions.iloc[i]
        writeRobtarget(i, position)    
        writeMoveL(i)

    with open(outputfile_robtargets,"w") as file:
        for line in robtargets:
            file.writelines(line)

    with open(outputfile_moveLs,"w") as file:
        for line in moveLs:
            file.writelines(line)

    print("Conversion finished")
    
    # Plot expected result
    plotPath()
    
    
if __name__ == "__main__":
   main(sys.argv[1:])



