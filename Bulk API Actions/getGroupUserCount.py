import requests
from requests.auth import HTTPBasicAuth
import json
import time

#prompt for URL and admin credentials

sURL= input("Server URL to connect to: ")
iUserName= input("Admin Username: ")
iPassword= input("Admin Password: ")

i=0

groups = []

gCount = []

gCountG = []


# API 1 get all groups with filter
url = "http://"+sURL+":8080/alfresco/service/api/rootgroups?"

headers = {
    'content-type': "application/json"
    }
        

response = requests.request("GET", url, headers=headers, auth=HTTPBasicAuth(iUserName,iPassword))

print(response.text)

jData = json.loads(response.content)
    
   

# Add all results of get group api into a list. also used index exception to avoid index out of bounds once last user is reached.
j = 0
end = False

while (end!=True):
    try:
        groups.append((str(jData['data'][j]['shortName'])))
        j+=1
    except IndexError:
        end=True
    


    
    
 
k=0 

for k in range(0,len(groups)):

    
    # API 2 query for each group returned in api 1. returns count of users.
    url2 = "http://"+sURL+":8080/alfresco/service/api/groups/"+groups[k]+"/children?authorityType=GROUP&sortBy=authorityName"

    headers2 = {
        'content-type': "application/json"
        }
        
    response2 = requests.request("GET", url2, headers=headers2, auth=HTTPBasicAuth(iUserName,iPassword))
    
    jData2 =json.loads(response2.content)
    
    
    gCountG.append(int(jData2['paging']['totalItems']))
 
 
 
 
 
l=0 

for l in range(0,len(groups)):

    
    # API 3 query for each group returned in api 1. returns count of users.
    url3 = "http://"+sURL+":8080/alfresco/service/api/groups/"+groups[l]+"/children?authorityType=USER&sortBy=authorityName"

    headers3 = {
        'content-type': "application/json"
        }
        
    response3 = requests.request("GET", url3, headers=headers3, auth=HTTPBasicAuth(iUserName,iPassword))
    
    jData3 =json.loads(response3.content)
    
    
    gCount.append(int(jData3['paging']['totalItems']))
    
    
    
#blank out file first before writing.
f = open('groupCount.csv','w').close()
#open file to write output to
f = open('groupCount.csv','w')


f.write("GROUPS: \n")
for m in range(0,len(groups)):
    f.write(groups[m]+' : '+str(gCountG[m])+'\n')
    
    
f.write("\n\n\nUSERS: \n")
for n in range(0,len(groups)):
    f.write(groups[n]+' : '+str(gCount[m])+'\n')
    
    
f.write("\n\n\nTOTAL CHILDREN: \n")
for o in range(0,len(groups)):
    f.write(groups[o]+' : '+str(gCount[o]+gCountG[o])+'\n')