##############################################
#
# Created by Grayson Cody Collins
#
# Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3
# with any questions, improvements, or requests.
#
##############################################



###IN PROGRESS, Continueing to use CURL for upload.
import requests
from requests.auth import HTTPBasicAuth
import json


 
 
 
 
 

url = "http://34.203.167.72:8080/activiti-app/api/enterprise/app-definitions/import"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"file\"; filename=\"test1.zip\"\r\nContent-Type: application/zip\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'authorization': "Basic YWRtaW5AYXBwLmFjdGl2aXRpLmNvbTphZG1pbg==",
    'cache-control': "no-cache",
    'postman-token': "cb5d8dcf-1cd4-744f-0a26-2b311627f8ef"
    }

response = requests.request("POST", url, data=payload, headers=headers,auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

print(response.text)