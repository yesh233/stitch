#! /usr/bin/env python

import sys
import os
from config import hdfsFolder,blendFileName,finalFileName

jobName = sys.argv[1]

redirectFile = hdfsFolder + jobName + "/commandInfo"
redirectCommand = " >>" + redirectFile + " 2>>" + redirectFile

if not os.path.exists(hdfsFolder + jobName):
	os.system("mkdir " +  hdfsFolder + jobName + " >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/blocks >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/imgs >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/labels >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/tmp >/dev/null 2>&1")

os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/" + blendFileName + " "  + hdfsFolder + jobName + redirectCommand)
os.chdir(hdfsFolder + jobName)

for line in sys.stdin:
	if line == '':
		continue
	handleInfo = line.split()	
	os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/tmp/" + handleInfo[0] + ".jpg " + hdfsFolder + jobName + "/tmp/" + redirectCommand)

command = "/home/mfkiller/stitch/bin/blend " + finalFileName + redirectCommand
os.system(command)
os.system("$HADOOP_HOME/bin/hadoop fs -put " + hdfsFolder + jobName + "/" + finalFileName + " " + jobName + "/" + redirectCommand)
