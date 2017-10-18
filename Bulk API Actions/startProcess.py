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
# This is a python script that is used to start processes in bulk
#
##############################################

import requests
from requests.auth import HTTPBasicAuth
import json
import time


#API start process
for i in range(0,1000):
 
    # API 1 create groups
    url = "http://54.167.179.17:8080/activiti-app/api/enterprise/process-instances"

    headers = {
        'content-type': "application/json"
        }
        
    payload = "{\r\n\"processDefinitionId\": \"test2:1:2504\",\r\n\"businessKey\" : \"test2\"\r\n}"
    
    response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

    print(response.text)
