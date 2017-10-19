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
# This is a python script used to collect a list of list of task ids
# then to use the list of lists in multithreaded request calls to complete the tasks
#
##############################################

import threading
import requests
from requests.auth import HTTPBasicAuth
import json

#tasksT = []

#function for completing set of processes in thread
def form_thread ( count):
    tasks = []
    
    # API 1 get all currently running tasks in batches of 100. use count for pagination
    url = "http://54.167.179.17:8080/activiti-app/api/enterprise/tasks/query"

    headers = {
        'content-type': "application/json"
    }
            
    payload = "{\n\"appDefinitionId\":1001,\n\"size\":\"100\",\n\"start\":"+str(count)+",\n\"state\":\"active\"\n}"
            
    response = requests.request("POST", url, data=payload, headers=headers, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

    #print(response.text)

    jData = json.loads(response.content)
        
       

    # Add all results of get running task api into a list. also used index exception to avoid index out of bounds once last task is reached.
    j = 0
    end = False

    while (end!=True):
        try:
            tasks.append(str(jData['data'][j]['id']))
            j+=1
        except IndexError:
            end=True

            
    #tasksT.append(tasks)

    #API 2 complete the processes using the tasks list
    for i in range(0,len(tasks)):
     
        # API 2 complete task
        url2 = "http://54.167.179.17:8080/activiti-app/api/enterprise/tasks/"+tasks[i]+"/action/complete"

        headers2 = {
            'content-type': "application/json",

        }

        response2 = requests.request("PUT", url2, headers=headers2, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

        
        #if (i==99):
            #print(response2.text)
        
        
    print("######################")
    print(str(count)+" thread complete")
    print("######################")
    
    
threads = []

for i in range(0,2):
    
    t = threading.Thread(target=form_thread(i))
    threads.append(t)
    t.start()
    
    
