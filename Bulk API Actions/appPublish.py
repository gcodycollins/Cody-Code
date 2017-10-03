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

for i in range (0, 10):

 url = "http://192.168.11.133:8080/activiti-app/api/enterprise/models/"

 payload = "{\r\n    \"modelType\": 3,\r\n    \"name\": \"Test1\"\r\n}\r\n"
 headers = {
     'content-type': "application/json"
     }

 response = requests.request("POST", url, data=payload, headers=headers,auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

 print(response.text)

 jData = json.loads(response.content)

 apId=(str(jData['id']))


 url2 = "http://192.168.11.133:8080/activiti-app/api/enterprise/app-definitions/"+apId

 payload2 = "{\"appDefinition\":{\"id\":"+apId+",\"name\":"+apId+",\"description\":\"\",\"version\":1,\"created\":\"2017-05-11T17:36:41.561+0000\",\"definition\":{\"models\":[{\"id\":1003,\"name\":\"testAppModel\",\"version\":2,\"modelType\":0,\"description\":null,\"stencilSetId\":null,\"createdByFullName\":\" Administrator\",\"createdBy\":1,\"lastUpdatedByFullName\":\" Administrator\",\"lastUpdatedBy\":1,\"lastUpdated\":\"2017-05-11T15:32:02.473+0000\"}],\"theme\":\"theme-1\",\"icon\":\"glyphicon-asterisk\",\"publishIdentityInfo\":[]}},\"publish\":true,\"force\":true}"
 headers2 = {
     'content-type': "application/json"
     }

 response2 = requests.request("PUT", url2, data=payload2, headers=headers2,auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

 print(response2.text)
 i+=1