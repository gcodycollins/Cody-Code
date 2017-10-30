##############################################
#
# Created by Grayson Cody Collins
#
# Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3
# with any questions, improvements, or requests.
#
##############################################

##############################################
#
# The function of this python script is to parse an activiti.log file.
# The process uses custom execution listeners to log timestamps of when the process has started and ended
# This script utilizes the output to get the average process execution time as well as
# the total time from first process start to last process completion
#
##############################################


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
with open('activiti.log') as logSample:

    #set each line to its own var in dictionary logs
    for line in logSample:
    
        # check for [Process= in the line, ignore the line if it doesn't have this    
        if (r'[Process=' in line):
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
        

    #Parse each line in log{} and return whatever is between Process= and ][  , which will leave you with process id
    for j in range (0,len(logs)):
        #sj=str(j)
        start = logs[j].find('Process=')+8
        end = logs[j].find('][', start)
        process[j]=logs[j][start:end]
        #print ('process'+sj+'= '+process[j])
    
    #blank out file first before writing.
    f = open('ProcessExecutionStats.txt','w').close()
    #open file to write output to
    f = open('ProcessExecutionStats.txt','w')
    
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
                
                
                #f.write(str(execTime)+' ms to complete Process '+process[j]+'\n')
                
                #print (str(execTime)+' ms to complete Process '+process[j])
                processes+=1
    
    #Divide execAverage by half of the length of dictionary logs. half of length of logs{} equals to total number of processes
    execAverage=execAverage/(len(logs)/2)
    
    #Calculate the total time between first start event and last end event.
    totalExecution=timeMS[len(timeMS)-1]-timeMS[0]
    
    f.write('Total process execution time is '+str(totalExecution)+' ms')
    print ('Total process execution time is '+str(totalExecution)+' ms')
    
    f.write('\nAverage process execution time is '+str(execAverage)+' ms')
    print ('Average process execution time is '+str(execAverage)+' ms')
    
    f.write('\nTotal number of processes is: '+str(processes)+'\n\n')
    print ('Total number of processes is: '+str(processes))
    #print (str(len(logs)/2))
    
    
    #same loop logic previously used. Simply moved output below the totatlExectuion, executionaverage and number of processes for output file
    for j in range (0,len(logs)):
        for k in range (0,len(logs)):
            if (process[j]==process[k] and j<k):
            
                execTime=timeMS[k]-timeMS[j]
                #add all execTimes to execAverage
                execAverage+=execTime
                
               
                f.write(str(execTime)+' ms to complete Process '+process[j]+'\n')
                
                print (str(execTime)+' ms to complete Process '+process[j])
                processes+=1
            
    f.close()