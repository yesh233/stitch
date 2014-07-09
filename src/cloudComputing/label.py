#! /usr/bin/env python

import sys
import os
from config import hdfsFolder,argFileName,planeFileName,bundleFileName

jobName = sys.argv[1]

redirectFile = hdfsFolder + jobName + "/commandInfo"
redirectCommand = " >>" + redirectFile + " 2>>" + redirectFile

if not os.path.exists(hdfsFolder + jobName):
	os.system("mkdir " +  hdfsFolder + jobName + " >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/blocks >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/imgs >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/labels >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/tmp >/dev/null 2>&1")
	
os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/" + argFileName + " "  + hdfsFolder + jobName + redirectCommand)
os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/" + planeFileName + " "  + hdfsFolder + jobName + redirectCommand)
os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/" + bundleFileName + " "  + hdfsFolder + jobName + redirectCommand)
os.chdir(hdfsFolder + jobName)

for line in sys.stdin:
	if line == '':
		continue
	handleInfo = line.split()	
	
	command = "/home/mfkiller/stitch/bin/label " + handleInfo[0] + ' ' + handleInfo[1] + ' ' + handleInfo[2] +  \
		 ' ' + handleInfo[3] + ' ' + handleInfo[4] + redirectCommand
	os.system(command)
	os.system("$HADOOP_HOME/bin/hadoop fs -put " + hdfsFolder + jobName + "/blocks/" + handleInfo[0] + ".txt " + jobName + "/blocks/" + redirectCommand)
	os.system("$HADOOP_HOME/bin/hadoop fs -put " + hdfsFolder + jobName + "/labels/" + handleInfo[0] + ".bmp " + jobName + "/labels/" + redirectCommand)

