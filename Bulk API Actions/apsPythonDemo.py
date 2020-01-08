#!/usr/local/bin/python3

#APS python Demo

#created by Cody Collins

import requests
from requests.auth import HTTPBasicAuth
import json

#default iterator
i=0
#baseURL
baseURL=r"http://localhost:8080/activiti-app/api/enterprise"





#API 1 Get process definition ID
url1 = baseURL+r"/process-definitions"

print("\n\n\nMaking API call:\n"+str(url1))

headers1 = {
    'content-type': "application/json"
    }

response1 = requests.request("GET", url1, headers=headers1, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

jData1 = json.loads(response1.text)

print("\n\n\n"+str(jData1))





'''
part2
'''
procDefID = str(jData1['data'][i]['id'])

print ("\n\n\nprocDefID\n"+procDefID)

#API 2 start process off of returned model
url2 = baseURL+r"/process-instances"

print("\n\n\nMaking API call:\n"+str(url2))

headers2 = {
    'content-type': "application/json"
    }

payload2 = "{\r\"processDefinitionId\": \""+procDefID+"\"}"

response2 = requests.request("POST", url2, headers=headers2, data=payload2, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

jData2 = json.loads(response2.text)

print("\n\n\n"+str(jData2))
'''
/part2
'''





'''
part3
'''
procInstanceID = str(jData2['id'])

print ("\n\n\nprocInstanceID\n"+procInstanceID)

#API 3 to get task ID of the started process Instance
url3 = baseURL+r"/tasks/query"

print("\n\n\nMaking API call:\n"+str(url3))

headers3 = {
    'content-type': "application/json"
    }

payload3 = "{\"processInstanceId\":"+procInstanceID+"}"

response3 = requests.request("POST", url3, headers=headers3, data=payload3, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

jData3 = json.loads(response3.text)

print("\n\n\n"+str(jData3))
'''
/part3
'''




'''
part4
'''
taskID = str(jData3['data'][i]['id'])

print ("\n\n\ntaskID\n"+taskID)

#API 4 to complete the form using returned task ID
url4 = baseURL+r"/task-forms/"+taskID

print("\n\n\nMaking API call:\n"+str(url4))

headers4 = {
    'content-type': "application/json"
    }

payload4 = "{\"values\": {\"label\":\"Completed\", \"label1\":\"By\", \"label2\":\"Python\" }}"

response4 = requests.request("POST", url4, headers=headers4, data=payload4, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

#jData4 = json.loads(response4.text)

print("\n\n\n"+str(response4.text))
print("\n\n\n#####\nTask Completed")
'''
/part4
'''