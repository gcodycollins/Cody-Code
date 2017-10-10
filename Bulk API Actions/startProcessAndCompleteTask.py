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
# This Pyhton script is used to start a process with a user task and then make 
# a second API call to compelte the task.
#
##############################################



import requests
from requests.auth import HTTPBasicAuth
import json
import time

tasks = []

#loop to batch execution 
for h in range(0,1):

    #API 1 start the processes
    for i in range(0,1000):
     
        # API 1 start process
        url = "http://54.175.46.136:8080/activiti-app/api/enterprise/process-instances"

        headers = {
            'content-type': "application/json"
            }

        payload = "{\r\n\"processDefinitionId\": \"histLoader:1:4\",\r\n\"businessKey\" : \"histLoader\"\r\n}"

        response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

        #print(response.text)

        
        
        
    # API 2 get all currently running tasks
    url2 = "http://54.175.46.136:8080/activiti-app/api/enterprise/tasks/query"

    headers2 = {
        'content-type': "application/json"
        }
            
    payload2 = "{\n\t\"appDefinitionId\":1,\n\t\"size\":\"1000\",\n\t\"state\":\"active\"\n}"
            
    response2 = requests.request("POST", url2, headers=headers2, data=payload2, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

    #print(response2.text)

    jData = json.loads(response2.content)
        
       

    # Add all results of get running task api into a list. also used index exception to avoid index out of bounds once last user is reached.
    j = 0
    end = False

    while (end!=True):
        try:
            tasks.append(str(jData['data'][j]['id']))
            j+=1
        except IndexError:
            end=True
        

    #taskString= ' '.join(tasks)
    #print ("taskString: "+taskString)




    #API 3 complete the processes using
    for i in range(0,len(tasks)):
     
        # API 3 complete task
        url3 = "http://54.175.46.136:8080/activiti-app/api/enterprise/tasks/"+tasks[i]+"/action/complete"

        headers3 = {
            'content-type': "application/json",

        }

        response3 = requests.request("PUT", url3, headers=headers3, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

        #print(response3.text)

    print("###########################")
    print(str(h))
    print("###########################")