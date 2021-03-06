##############################################
#
# Created by Grayson Cody Collins
#
# Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3
# with any questions, improvements, or requests.
#
##############################################


#initialize vars
logs={}
groupName={}
groupSize={}
i=0
j=0
total=0

#open log file
with open('groupCountTotal.csv') as groupCount:

    #set each line to its own var in dictionary logs
    for line in groupCount:
        logs[i] = line
        i+=1
    
    #confim by printing each line in dictionary logs    
    #for j in range (0,len(logs)):
        #sj=str(j)
        #print ('logs'+sj+'= '+logs[j])

    #parse log{} and extract time to store in its own dictionary, store time in ms in its own dictionary
    for j in range (0,len(logs)):
        #sj=str(j)

        start = logs[j].find('')+0
        end = logs[j].find(' : ', start)
        
        groupName[j]=(logs[j][start:end])
        
        start2 = logs[j].find(' : ')+3
        
        groupSize[j]=(logs[j][start2:])
    
    
    #search the process dictionary for like values, when like values are found, subtract the times leaving you with execution time per process
    for j in range (0,len(logs)):
    
        total += int(groupSize[j])
        
    print("Total Children: "+str(total))