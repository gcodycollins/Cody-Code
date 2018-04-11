'''
Contact:
 Created by Grayson Cody Collins
 Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3 with any questions, improvements, or requests.

Purpose:
 The Function of this code is to gather APS configurations and statistics.

Wishlist/future feature tracker for my own personal memory:
 -SQL code execution against configured DB, DB vendor specific SQL based on pulled properties.
 -When pulling certain properties, logic to go and get other files to get related configs.
 -Logic to pre-emptively inform customer for recommendation? Or do all of that on our end?
 -Logic to handle if the DB url contains variables like ${dbName}. Retrieve those variables too.
 -Handle multiple of the same properties, only read the last logged one just like in spring.
 
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
    
    
    

    
#New Def
    
#######################   
### End Definitions ###
#######################










#Check if Windows
if os.name =='nt':
    windows=True

#Execute if Windows    
if windows:

    #get all drive letters
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
        



        
    #Declare default values for properties
    datasourceDriver="datasource.driver="
    datasourceUrl="datasource.url="
    datasourceUsername="datasource.username="
    datasourcePassword="datasource.password="
    hibernateDialect="hibernate.dialect="
        
    #Open the found activiti-app.properties file
    with open(actAppProp) as appProp:
    
        print("Reading File: "+actAppProp)
    
        #parse the file line by line. This also ensures that when the same property is uncommented, it will always pick up the 
        #last uncommented property just like spring does
        for line in appProp:
        
            #Pull DB Properties.          
            if (r'datasource.driver=' in line and not "#" in line):
                #HC.write(line+'\n')
                datasourceDriver=line
                
            elif(r'datasource.url=' in line and not "#" in line):
                #HC.write(line+'\n')
                datasourceUrl=line
                
            elif(r'datasource.username=' in line and not "#" in line):
                #HC.write(line+'\n')
                datasourceUsername=line
                
            elif(r'datasource.password=' in line and not "#" in line):
                #HC.write(line+'\n')
                datasourcePassword=line
                
            elif(r'hibernate.dialect=' in line and not "#" in line):
                #HC.write(line+'\n')
                hibernateDialect=line
                
                
                
    
    
    #Open file to begin writing all useful HC information to
    #blank out file first before writing.
    HC = open('HCInfo.txt','w').close()
    #open file to write output to
    HC = open('HCInfo.txt','w')
    
    print("Writing File: HCInfo.txt")
    
    #Write HC file with pre filled properties to account for when multiple are found.
    HC.write('###########################\n### Database Properties ###\n###########################\n')
    HC.write(datasourceDriver+'\n')
    HC.write(datasourceUrl+'\n')
    HC.write(datasourceUsername+'\n')
    HC.write(datasourcePassword+'\n')
    HC.write(hibernateDialect+'\n')