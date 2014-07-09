#! /usr/bin/env python

import sys
import os
import time
import config

'''
generate hadoop streamming command
'''

jobName = sys.argv[1]
mapTaskCount = int(sys.argv[2])
nx = sys.argv[3]
ny = sys.argv[4]

logFile = config.logFolder + jobName + '.log'
redirectCommand = ' >' + logFile + ' 2>&1'

#mkdir local
os.system("mkdir " +  config.hdfsFolder + jobName + " >/dev/null 2>&1")
os.system("mkdir " +  config.hdfsFolder + jobName + "/blocks >/dev/null 2>&1")
os.system("mkdir " +  config.hdfsFolder + jobName + "/imgs >/dev/null 2>&1")
os.system("mkdir " +  config.hdfsFolder + jobName + "/labels >/dev/null 2>&1")
os.system("mkdir " +  config.hdfsFolder + jobName + "/tmp >/dev/null 2>&1")

#mkdir hdfs
os.system("$HADOOP_HOME/bin/hadoop fs -mkdir " + jobName + "/blocks" + redirectCommand)
os.system("$HADOOP_HOME/bin/hadoop fs -mkdir " + jobName + "/labels" + redirectCommand)
os.system("$HADOOP_HOME/bin/hadoop fs -mkdir " + jobName + "/tmp" + redirectCommand)

#chdir
os.chdir(config.hdfsFolder + jobName)

#get arg bundle
os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/" + config.argFileName + " " + config.hdfsFolder + jobName + redirectCommand)
os.system("$HADOOP_HOME/bin/hadoop fs -get " + jobName + "/" + config.bundleFileName + " " + config.hdfsFolder + jobName + redirectCommand)

#calc plane
command = "/home/mfkiller/stitch/bin/plane " + redirectCommand
os.system(command)
os.system("$HADOOP_HOME/bin/hadoop fs -put " + config.planeFileName+ " " + jobName + "/" + redirectCommand)

#gen
command = "/home/mfkiller/stitch/bin/gen " + nx + " " + ny + redirectCommand
os.system(command)
os.system("$HADOOP_HOME/bin/hadoop fs -put " + config.blockFileName+ " " + jobName + "/" + redirectCommand)
os.system("$HADOOP_HOME/bin/hadoop fs -put " + config.blendFileName+ " " + jobName + "/" + redirectCommand)
os.system("$HADOOP_HOME/bin/hadoop fs -put " + config.labelFileName+ " " + jobName + "/" + redirectCommand)
	
#label
hadoopCommand = ("$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-1.0.4.jar \
-D mapred.map.tasks=%d -D mapred.reduce.tasks=0 \
-input %s/%s -output %s/label_output \
-file %s -file %s -mapper '%s %s'  %s") % \
(mapTaskCount, jobName, config.labelFileName, jobName,config.configFilePath, config.labelFilePath, config.labelFilePath, jobName, redirectCommand)
os.system(hadoopCommand)


#image blend
hadoopCommand = ("$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-1.0.4.jar \
-D mapred.map.tasks=%d -D mapred.reduce.tasks=1 \
-input %s/%s -output %s/image_output \
-file %s -file %s -mapper '%s %s' -file %s -reducer '%s %s' %s") % \
(mapTaskCount, jobName, config.blockFileName, jobName,config.configFilePath, config.imageFilePath, config.imageFilePath, jobName, config.blendFilePath, config.blendFilePath, jobName, redirectCommand)

os.system(hadoopCommand)

