import requests
from requests.auth import HTTPBasicAuth
import json
import time

#prompt for # of users, # of groups, URL, and admin credentials

gCount= input("Number of groups to create: ")
uCount= input("Number of users to create: ")
gName= input("Name of groups to create: ")
uName= input("Name of users to create: ")
sURL= input("Server URL to connect to: ")
iUserName= input("Admin Username: ")
iPassword= input("Admin Password: ")

i=0
userName = []
groups = []

#number of groups to create
for i in range(0,int(gCount)):

    

    
    # API 1 create groups
    url = "http://"+sURL+":8080/alfresco/service/api/rootgroups/"+gName+str(i)

    headers = {
        'content-type': "application/json"
        }
        
    payload = "{\r\n\r\n}"

    response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth(iUserName,iPassword))

    print(response.text)
    


    
 


#wait a few seconds to allow groups and users to populate in response
time.sleep(30)





# API 2 get all groups with filter
url2 = "http://"+sURL+":8080/alfresco/service/api/rootgroups?shortNameFilter="+gName+"*&maxItems=1000"

headers2 = {
    'content-type': "application/json"
    }
        

response2 = requests.request("GET", url2, headers=headers2, auth=HTTPBasicAuth(iUserName,iPassword))

print(response2.text)

jData = json.loads(response2.content)
    
   

# Add all results of get group api into a list. also used index exception to avoid index out of bounds once last user is reached.
j = 0
end = False

while (end!=True):
    try:
        groups.append('"'+(str(jData['data'][j]['fullName']))+'", ')
        j+=1
    except IndexError:
        end=True
    
groups.append("\"filler\"") #intentional dummy group to avoid end comma in group array
groupString= ''.join(groups)

#print ("GroupString: "+groupString)
 
 
 
 
 
 
 
k=0 
#number of users to create
for k in range(0,int(uCount)):

 
    user=uName+str(k)
    
    userName.append(user)
    
    # API 3 create users
    url3 = "http://"+sURL+":8080/alfresco/service/api/people"

    headers3 = {
        'content-type': "application/json"
        }
        
    payload3="{\r\n\t\"userName\":\""+user+"\",\r\n\t\"firstName\":\""+user+"\",\r\n\t\"lastName\":\""+user+"\",\r\n\t\"email\":\""+user+"@"+user+"."+user+"\",\r\n\t\"groups\":["+groupString+"]\r\n}"
    #print ("payload3: "+payload3)

    response3 = requests.request("POST", url3, headers=headers3, data=payload3, auth=HTTPBasicAuth(iUserName,iPassword))

    print(response3.text)
