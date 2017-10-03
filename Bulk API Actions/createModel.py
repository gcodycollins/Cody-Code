##############################################
#
# Created by Grayson Cody Collins
#
# Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3
# with any questions, improvements, or requests.
#
##############################################


import requests
from requests.auth import HTTPBasicAuth
import json


headers = {
 'authorization': "Basic YWRtaW5AYXBwLmFjdGl2aXRpLmNvbTphZG1pbg==",
 'content-type': "application/json",
 'cache-control': "no-cache"
}

j=0
for j in range (0,10):
 payload = "{\r\n    \"modelType\": 0,\r\n    \"name\": \"testAppModel"+str(j)+"\"\r\n}"
 url = "http://34.203.167.72:8080/activiti-app/api/enterprise/models/"
 response = requests.request("POST", url, data=payload, headers=headers)
 j+=1
