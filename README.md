# GCode-to-ABB
A python implementation for transforming a GCode file to a ABB robot specific movements.
<p align="center">
  <img src="Examples/ABB robot drawing.gif"  alt="ABB robot drawing.gif" width=400><br/>
  <i> Result of the script </i>
</p>

## Introduction
This repository contains a Python script that generates the points and movement commands for ABB robots from a GCode of a 2D object.

## How to use
Open a terminal and run the python script with the file you want to convert with the `-i` option. You can also change the output file names with the `-o` option. 

    python GCode_to_Robtargets.py -i inputfile
    python GCode_to_Robtargets.py -i inputfile -o outputfile

As a result you will obtain two files containing all the points and the lineal movements that will be performed by the robot. You just should load these lines to your ABB robot´s program and call them.

You can also specify the rotation and configuration of the robot axis with the `-r` and `-c` options respectively.

    python GCode_to_Robtargets.py -i inputfile -r [-1,0,0,0]
    python GCode_to_Robtargets.py -i inputfile -c [-1,0,1,0]

## Future functionalities
In the current version, the script only parses `G00` and `G01` (linear movements). In future releases I would like to add more GCode commands (such as `G02`, `G03` (arc movements) and `G04` (dwell)).

## Requirements
You should install the following:

* Python
* Matplotlib
* Numpy
* Pandas
* Mpl_toolkits

## For Developers and coders!
I am aware that some parts could be optimized or are redundant for such small program. However I decided to make it as easy and simple as possible for anybody who is new to programming.

