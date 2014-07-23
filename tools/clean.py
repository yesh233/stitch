import os
import sys

jobName = sys.argv[1]
hostNames = ['Slave1']
hdfsFolder = '/home/mfkiller/stitch/hdfs/'


for hostName in hostNames:
	cleanCommand = ('''ssh %s "rm -rf %s%s"''') % (hostName, hdfsFolder, jobName)
	os.system(cleanCommand)

hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rmr " + jobName + "/blocks"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rmr " + jobName + "/labels"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rmr " + jobName + "/tmp"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rmr " + jobName + "/label_output"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rmr " + jobName + "/image_output"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rm " + jobName + "/blend.txt"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rm " + jobName + "/block.txt"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rm " + jobName + "/label.txt"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rm " + jobName + "/plane.txt"
os.system(hdfsClean)
hdfsClean = "$HADOOP_HOME/bin/hadoop fs -rm " + jobName + "/final.jpg"
os.system(hdfsClean)
