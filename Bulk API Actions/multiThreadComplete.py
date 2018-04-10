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
# then to use the list of lists in multithreaded/multiprocessed request calls to complete the tasks
#
# MultiProcessing is working, it still is not just very fast. Need to review how task IDs are gotten in the first place.
#
##############################################


import threading
import requests
from requests.auth import HTTPBasicAuth
import json
import multiprocessing
from multiprocessing import Pool









#function for completing set of processes in thread
def form_thread (count):

    serverURL="http://54.175.46.136:9090"

    #this will be a list of lists
    #tasksT = []
    
    #this is a list of all task IDs in the below api call
    tasks = []
        
    # API 1 get all currently running tasks in batches of 100. use count for pagination
    url = serverURL+"/activiti-app/api/enterprise/tasks/query"

    headers = {
        'content-type': "application/json"
    }
                
    payload = "{\n\"appDefinitionId\":2002,\n\"size\":\"500\",\n\"start\":"+str(count)+",\n\"state\":\"active\"\n}"
                
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

    #add the list to the list of lists
    #tasksT.append(tasks)
    
    print("######################")
    print(str(count)+" TaskIDs Loaded")
    print("######################")


        
        

    #API 2 complete the processes using the tasks list
    for i in range(0,len(tasks)):
         
        # API 2 complete task
        
        #plain task no form
        #url2 = serverURL+"/activiti-app/api/enterprise/tasks/"+tasks[i]+"/action/complete"
        
        #task with form
        url2 = serverURL+"/activiti-app/api/enterprise/task-forms/"+tasks[i]

        headers2 = {
            'content-type': "application/json",

        }
        
        payload2 = "{\n\t\"values\":{\n\t\t\"label\":\"label\",\n\t\t\"label1\":\"label1\",\n\t\t\"label2\":\"label2\",\n\t\t\"label3\":\"label3\",\n\t\t\"label4\":\"label4\",\n\t\t\"label5\":\"label5\",\n\t\t\"label6\":\"label6\",\n\t\t\"label7\":\"label7\",\n\t\t\"label8\":\"label8\",\n\t\t\"label9\":\"label9\",\n\t\t\"label10\":\"label10\",\n\t\t\"label11\":\"label11\",\n\t\t\"label12\":\"label12\",\n\t\t\"label13\":\"label13\",\n\t\t\"label14\":\"label14\",\n\t\t\"label15\":\"label15\",\n\t\t\"label16\":\"label16\",\n\t\t\"label17\":\"label17\",\n\t\t\"label18\":\"label18\",\n\t\t\"label19\":\"label19\",\n\t\t\"label20\":\"label20\",\n\t\t\"label21\":\"label21\",\n\t\t\"label22\":\"label22\",\n\t\t\"label23\":\"label23\",\n\t\t\"label24\":\"label24\",\n\t\t\"label25\":\"label25\",\n\t\t\"label26\":\"label26\",\n\t\t\"label27\":\"label27\",\n\t\t\"label28\":\"label28\",\n\t\t\"label29\":\"label29\",\n\t\t\"label30\":\"label30\",\n\t\t\"label31\":\"label31\",\n\t\t\"label32\":\"label32\",\n\t\t\"label33\":\"label33\",\n\t\t\"label34\":\"label34\",\n\t\t\"label35\":\"label35\",\n\t\t\"label36\":\"label36\",\n\t\t\"label37\":\"label37\",\n\t\t\"label38\":\"label38\",\n\t\t\"label39\":\"label39\",\n\t\t\"label40\":\"label40\",\n\t\t\"label41\":\"label41\",\n\t\t\"label42\":\"label42\",\n\t\t\"label43\":\"label43\",\n\t\t\"label44\":\"label44\",\n\t\t\"label45\":\"label45\",\n\t\t\"label46\":\"label46\",\n\t\t\"label47\":\"label47\",\n\t\t\"label48\":\"label48\",\n\t\t\"label49\":\"label49\"\n\t}\n}"


        response2 = requests.request("POST", url2, headers=headers2, data=payload2, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

            
        if (i==0):
            print(response2.text)
                   
    print("######################")
    print(str(count)+" thread complete")
    print("######################")






for k in range (0,10):

       
        
    threads = [0,1,2,3,4,5,6,7,8,9]

    #multithreaded processing
    #for i in range(0,threadnum):
    
    if __name__ == "__main__":
        
        pool = Pool(processes=10)
        result = pool.map(form_thread, threads)