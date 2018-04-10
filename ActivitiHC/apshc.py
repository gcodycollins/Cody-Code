'''
Contact:
 Created by Grayson Cody Collins
 Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3 with any questions, improvements, or requests.

Purpose:
 The Function of this code is to gather APS configurations and statistics.

Wishlist/future feature tracker for my own personal memory:
 -SQL code execution against configured DB, DB vendor specific SQL based on pulled properties.
 -Logic to pre-emptively inform customer for recommendation? Or do all of that on our end?
 -Logic to handle if the DB url contains variables like ${dbName}. Retrieve those variables too.
 
Assumptions/Other:
 This code was developed using Python 3 branch.

'''
#Imports
import os
import fnmatch
import glob

from datetime import datetime
    
    
    
    
    
    
    
    
    
####################### 
###   Definitions   ###
#######################

#find specific files in (hopefully) the correct APS directory
def findFile(pattern):


    print("Searching for file matching "+pattern)
    result = glob.glob(pattern, recursive=True)

    return result;
    
    
    
    
    
#Source: http://opensourceforu.com/2016/10/file-search-with-python/
#Used for Windows to get all current drives. In case APS is on D: or other non-C: drive 
def get_drives():
    response = os.popen("wmic logicaldisk get caption")
    list1 = []
    total_file = []
    t1= datetime.now()
    for line in response.readlines():
        line = line.strip("\n")
        line = line.strip("\r")
        line = line.strip(" ")
        line = line.strip("'")
        if (line == "Caption" or line == ""):
            continue
        list1.append(line)
    return list1
    
#######################   
### End Definitions ###
#######################










#Check if Windows
if os.name =='nt':
    windows=True

#Execute if Windows    
if windows:

    drives= get_drives()

    results=[]
    
    for drive in drives:
        results += findFile(drive+'/**/tomcat/lib/activiti-app.properties')
     
    #handle if there is more than one possible APS environment found
    if (len(results)>1):
    
        print("\n\nMore than one possible APS Environment found.\n")
        
        for i in range (0,len(results)):
            
            print (str(i)+": "+results[i])
        
        #prompt for user input of correct path choice
        envChoice= input("\nEnter number of correct APS: ")
        
        #set variable equal to chosen file
        actAppProp=results[int(envChoice)]
        
    #else for if just one result of activiti-app.properties found    
    else:
    
        actAppProp=results[0]
        
    print(actAppProp)
    
    #Open file to begin writing all useful HC information to
    #blank out file first before writing.
    HC = open('HCInfo.txt','w').close()
    #open file to write output to
    HC = open('HCInfo.txt','w')
    
    j=0
    #Open the found activiti-app.properties file
    with open(actAppProp) as appProp:
    
        #parse the file line by line
        for line in appProp:
        
            j+=1
            print (j)