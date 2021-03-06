#! /usr/bin/env python

import sys
import os
from config import hdfsFolder

jobName = sys.argv[1]

redirectFile = hdfsFolder + jobName + "/commandInfo"
redirectCommand = " >>" + redirectFile + " 2>>" + redirectFile

if not os.path.exists(hdfsFolder + jobName):
	os.system("mkdir " +  hdfsFolder + jobName + " >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/blocks >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/imgs >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/labels >/dev/null 2>&1")
	os.system("mkdir " +  hdfsFolder + jobName + "/tmp >/dev/null 2>&1")
	
os.chdir(hdfsFolder + jobName)
for line in sys.stdin:
	if line == '':
		continue
	handleInfo = line.split()
	
	os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/blocks/" + handleInfo[0] + ".txt " + hdfsFolder + jobName + "/blocks/" + redirectCommand)
	os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/labels/" + handleInfo[0] + ".bmp " + hdfsFolder + jobName + "/labels/" + redirectCommand)
	
	f = open("blocks/"+handleInfo[0]+".txt", "r")
	fline = f.readline()
	f.close()
	
	imgs = fline.split()
	for img in imgs:
		os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/imgs/" + img + ".jpg " + hdfsFolder + jobName + "/imgs/" + redirectCommand)
			 
	command = "/home/mfkiller/stitch/bin/image " + handleInfo[0] + redirectCommand
	os.system(command)
	os.system("$HADOOP_HOME/bin/hadoop fs -put " + hdfsFolder + jobName + "/tmp/" + handleInfo[0] + ".jpg " + jobName + "/tmp/" + redirectCommand)
	print handleInfo[0]

