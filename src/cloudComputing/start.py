import os
import time
import sys
from ConfigParser import ConfigParser
from config import configFileName, coorFileName,adjFileName,bundlersrcFolder,\
     cloudsrcFolder, logFolder, bundlerFileName, argFileName, bundleFileName,\
     finalFileName

def config_parser(jobName):
    config = ConfigParser()
    config.read('../../input/'+jobName+'/'+configFileName)
    mapTaskCount = config.get('cloud','mapTaskCount')
    nx = config.get('cloud', 'nx')
    ny = config.get('cloud', 'ny')
    height = config.get('stitch', 'height')
    width = config.get('stitch', 'width')
    scale = config.get('stitch', 'scale') 
    sep = config.get('stitch', 'sep') 
    zoom = config.get('stitch', 'zoom') 
    times = config.get('plane', 'times') 
    thread = config.get('plane', 'thread') 
    #print mapTaskCount, nx, ny, height, width, scale, sep, zoom, times, thread
    return  mapTaskCount, nx, ny, height, width, scale, sep, \
            zoom, times, thread

def make_tmp_dir(jobName):
    tmpdir = '../../tmp/'+jobName
    try:
        os.mkdir(tmpdir)
    except:
        pass
    return tmpdir
 
def write_arg_txt(jobName, tmpdir, height, width, scale, sep, zoom, \
                  times, thread):
    argtxt = tmpdir+'/'+argFileName
    with open(argtxt, 'w') as arg:
        arg.write(' '.join([height, width, scale, sep, zoom, times, \
                           thread]))

def make_tmp_imgs_dir(jobName):
    tmpimgsdir = '../../tmp/'+jobName+'/imgs'
    try:
        os.mkdir(tmpimgsdir)
    except:
        pass
    return tmpimgsdir
    
def imgs_reduce(jobName, tmpimgsdir, scale):
    imgsdir = '../../input/'+jobName+'/imgs/'
    percent = str(int(100/float(scale)))+'%'
    for root, dirs, files in os.walk(imgsdir):
        for idx, img in enumerate(files):
	    command = 'convert -resize '+percent+'x'+percent+\
                      ' '+imgsdir+img+' '+tmpimgsdir+'/'+img
            os.system(command)
       
def dis((x1,y1),(x2,y2)):
    return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
    
def find_adj(jobName):
    imgsdir = '../../input/'+jobName+'/imgs/'
    coorpath = '../../input/'+jobName+'/'+coorFileName
    adjpath = '../../tmp/'+jobName+'/'+ adjFileName
    d = {}
    with open(coorpath) as coor:
        for c in coor:
            c = c.split()
            d[int(c[0])] = (float(c[1]), float(c[2]))
    a = []
    for root, dirs, files in os.walk(imgsdir):
        for img in files:
            a.append(int(img[4:8]))
    a.sort()
    #print a
    with open(adjpath, 'w') as adj:
        adj.write(str(len(a))+'\n')
        for idx, x in enumerate(a):
            c = []
            for idy, y in enumerate(a[:idx]): 
                c.append((dis(d[x],d[y]),idy))
            c.sort()
            c = map(lambda (x,y): str(y), c[0:20])
            adj.write(str(len(c))+' '+' '.join(c)+'\n')
          
def bundler(jobName, tmpdir):
    os.chdir(tmpdir)
    logFile = logFolder+jobName+'.log'
    redirectCommand = ' >' + logFile + ' 2&>1'
    os.system(bundlersrcFolder + bundlerFileName)
    os.chdir(cloudsrcFolder)

def put_to_hdfs(jobName, tmpdir):
    logFile = logFolder+jobName+'.log'
    redirectCommand = ' >' + logFile + ' 2&>1'
    os.system("hadoop fs -mkdir " + jobName)
    os.system("hadoop fs -mkdir " + jobName + "/imgs")
    hdfsimgsdir = jobName + "/imgs/"
    imgsdir = '../../input/'+jobName+'/imgs/' 
    for root, dirs, files in os.walk(imgsdir):
        files.sort()
        print files
        for idx,img in enumerate(files):
            os.system("hadoop fs -put " + imgsdir+img + ' ' + \
               hdfsimgsdir+str(idx)+'.jpg')
    os.system("hadoop fs -put " + tmpdir + '/' + argFileName+ \
               ' ' + str(jobName) + '/')
    os.system("hadoop fs -put " + tmpdir + '/bundle/' +  \
               bundleFileName+  ' ' + str(jobName) + '/')
    
def stitch(jobName, mapTaskCount, nx, ny):
    command = 'python stitch.py ' + ' '.join([jobName, mapTaskCount, nx, ny])
    #print command
    os.system(command)

def make_output_dir(jobName):
    outputdir = '../../output/'+jobName
    try:
        os.mkdir(outputdir)
    except:
        pass
    return outputdir
 
def save_result(jobName, outputdir):
    command = 'hadoop fs -get '+jobName+'/'+finalFileName+' '+outputdir+'/'
    os.system(command)
    command = 'convert -rotate -90 ' + outputdir+'/'+finalFileName + ' '+ \
              outputdir+'/'+finalFileName
    os.system(command)
  
def main():
    print time.localtime(time.time())
    os.chdir(cloudsrcFolder)
    jobName = sys.argv[1]
    mapTaskCount, nx, ny, height, width, scale, sep, zoom, times, \
        thread = config_parser(jobName)
    tmpdir = make_tmp_dir(jobName)
    write_arg_txt(jobName, tmpdir, height, width, scale, sep, zoom, \
                  times, thread)
    tmpimgsdir = make_tmp_imgs_dir(jobName)
    imgs_reduce(jobName, tmpimgsdir, scale)
    find_adj(jobName) 
    bundler(jobName, tmpdir)
    put_to_hdfs(jobName, tmpdir)
    stitch(jobName, mapTaskCount, nx, ny)
    outputdir = make_output_dir(jobName)
    save_result(jobName, outputdir)  
    print time.localtime(time.time())

if __name__ == '__main__':
    main()





	
        

