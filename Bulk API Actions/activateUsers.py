import requests
from requests.auth import HTTPBasicAuth
import json

#while loop to account for more than 1,000 inactive users. Only 1000 results can be passed into 2nd api call 
inactiveLeft =1
while inactiveLeft >=0:

    userID = []

    
    # First Api call to get all users with status inactive. Also pass page size of 500, start 0, size 1000 and tenantId 1. All were required to get full results
    url = "http://34.203.167.72:8080/activiti-app/api/enterprise/admin/users?status=inactive&start=0&page=500&size=1000&tenantId=1"

    headers = {
        'content-type': "application/json"
        }

    response = requests.request("GET", url, headers=headers,auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

    #print(response.text)

    jData = json.loads(response.content)

    
    
   

    # Add all results of id into a list. also used index exception to avoid index out of bounds once last user is reached. This is also batched into 1000 users at a time
    i = 0
    end = False

    while (end!=True and i < 999):
        try:
            userID.append((str(jData['data'][i]['id'])))
            i+=1
        except IndexError:
            end=True

    inactiveUsers= ', '.join(userID)
  
    print (inactiveUsers)
    
    
    
    #check if there are 0 inactive users left. If so, break loop and exit.
    if len(inactiveUsers)==0:
        inactiveLeft=0
        break

    
    
    
    
    # API number 2 to pass the inactiveUsers as a string of list userID. Only 1000 users at a time.
    url2 = "http://34.203.167.72:8080/activiti-app/api/enterprise/admin/users"

    payload2 = "{\r\n        \"users\" : ["+inactiveUsers+"],\r\n        \"status\" : \"active\"\r\n}"
    headers2 = {
        'content-type': "application/json"
        }

    response2 = requests.request("PUT", url2, data=payload2, headers=headers2,auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

    print(response2.text)