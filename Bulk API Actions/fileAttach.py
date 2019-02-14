##############################################
#
# Created by Cody Collins
#
# Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3
# with any questions, improvements, or requests.
#
##############################################

##############################################
#
# This Python script is used to start a process with a start form and attach file
#
##############################################



import requests
from requests.auth import HTTPBasicAuth
import json
import sys


#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))
#print ('\n\n\n\n\n')

#store first arg as text, store second arg as file
textField=sys.argv[1]
fileField=sys.argv[2]

#strip the file name from the full path
fileNameIndex=fileField.rfind('\\')

fileName=fileField[fileNameIndex:]


#API0 to upload content to activiti
############
#CHANGE URL#
############
url0 = "http://localhost:8080/activiti-app/api/enterprise/content/raw"

#store file arg as files parameter for request call
files = {'file': open(fileField, 'rb')}

response0 = requests.request("POST", url0, files=files, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

#Debug
#print(response0.text)



#load the response into Json to get the file ID
jData = json.loads(response0.content)

fileId=jData['id']

#Debug
#print("\n\n\n\n\n"+str(fileId))


     
# API 1 start process with hardcoded URL
############
#CHANGE URL#
############
url1 = "http://localhost:8080/activiti-app/api/enterprise/process-instances"

headers1 = {
    'content-type': "application/json"
    }

    
############################################
#CHANGE processDefinitionId and businessKey#
############################################
payload1 = "{\n\t\"processDefinitionId\": \"filetest:1:5136\",\n\t\"businessKey\" : \"filetest\",\n\t\"values\":\n\t\t{\n\t\t\t\"text1\":\""+textField+"\",\n\t\t\t\"file1\":\""+str(fileId)+"\"\n\t\t}\n\t\n}"

response1 = requests.request("POST", url1, headers=headers1, data=payload1, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

#Debug
#print("\n\n\n\n\n"+response1.text)