#initialize vars
logs={}
time={}
timeMS={}
process={}
hr=0
mi=0
se=0
ms=0
totalMS=0
execTime=0
execAverage=0
i=0
j=0
k=0
processes=0

#open log file
with open('test2.txt') as logSample:

    #set each line to its own var in dictionary logs
    for line in logSample:
        logs[i] = line
        i+=1
    
    #confim by printing each line in dictionary logs    
    #for j in range (0,len(logs)):
        #sj=str(j)
        #print ('logs'+sj+'= '+logs[j])

    #parse log{} and extract time to store in its own dictionary, store time in ms in its own dictionary
    for j in range (0,len(logs)):
        #sj=str(j)
        time[j]=(logs[j][11:23])
        #print ('time'+sj+'= '+time[j])
        
        #get total ms by adding hour, min, sec, and ms. strip timestap for hour, minute, second, millisecond
        hr=int(time[j][0:2])
        #print ('hr= '+str(hr))
        mi=int(time[j][3:5])
        #print ('mi= '+str(mi))
        se=int(time[j][6:8])
        #print ('se= '+str(se))
        ms=int(time[j][9:12])
        #print ('ms= '+str(ms))
        #add everything to get total ms
        totalMS=(hr*3600000)+(mi*60000)+(se*1000)+ms
        timeMS[j]=totalMS
        #print ('totalMS'+sj+'= '+str(timeMS[j]))
        
    #parse process by index, no go if greater than 4 characters
#    for j in range (0,4):
#        sj=str(j)
#        process[j]=(logs[j][120:124])
#        print ('process'+sj+'= '+process[j])

    #Parse each line in log{} and return whatever is between Process= and ][  , which will leave you with process id
    for j in range (0,len(logs)):
        #sj=str(j)
        start = logs[j].find('Process=')+8
        end = logs[j].find('][', start)
        process[j]=logs[j][start:end]
        #print ('process'+sj+'= '+process[j])
    
    #blank out file first before writing.
    f = open('pythonOutput.txt','w').close()
    #open file to write output to
    f = open('pythonOutput.txt','w')
    
    #search the process dictionary for like values, when like values are found, subtract the times leaving you with execution time per process
    for j in range (0,len(logs)):
        for k in range (0,len(logs)):
            if (process[j]==process[k] and j<k):
                #sj=str(j)
                #sk=str(k)
                #for debugging
                #print ('time'+sj+'= '+time[j])
                #print ('time'+sk+'= '+time[k])
                
                execTime=timeMS[k]-timeMS[j]
                #add all execTimes to execAverage
                execAverage+=execTime
                
                
                f.write(str(execTime)+' ms to complete Process '+process[j]+'\n')
                
                print (str(execTime)+' ms to complete Process '+process[j])
                processes+=1
    
    #Divide execAverage by half of the length of dictionary logs. of of length of logs equals to total number of processes
    execAverage=execAverage/(len(logs)/2)
    
    f.write('Average process execution time is '+str(execAverage)+' ms')
    print ('Average process execution time is '+str(execAverage)+' ms')
    
    f.write('Total number of processes is: '+str(processes))
    print ('Total number of processes is: '+str(processes))
    #print (str(len(logs)/2))
    f.close()