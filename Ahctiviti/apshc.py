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

'''
#Imports
import os, fnmatch, glob
    
    
    
    
    
    
    
    
    
####################### 
###   Definitions   ###
#######################

def findFile(pattern, path):
    print ("Pattern: "+path)
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result;
    
#######################   
### End Definitions ###
#######################










#Check if Windows
if os.name =='nt':
    windows=True

#Execute if Windows    
if windows:

    print("test")

    results = findFile('activiti-app.properties', '*\\tomcat\\lib\\')
        
    for i in range (0,len(results)):
            
        print (str(i)+": "+results[i])