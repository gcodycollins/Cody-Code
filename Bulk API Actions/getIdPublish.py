import requests
from requests.auth import HTTPBasicAuth
import json

# Replace with the correct URL
url = "http://34.203.167.72:8080/activiti-app/api/enterprise/models?filter=myApps&modelType=3"

head = {'content-type: application/json'}

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
myResponse = requests.get(url,auth=HTTPBasicAuth('admin@app.activiti.com','admin'))
#print (myResponse.status_code)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
    
    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content)

	

	
    i = 0
    j = 0
    end = False
    idarr=[]
    while end!=True:
     try:
       idarr.append((str(jData['data'][i]['id'])))
       i+=1
     except IndexError:
      end=True

    for j in range (0, i):
     print (idarr[j])
     j+=1


    
     
     payload = "{\r\n    \"comment\": \"\",\r\n    \"force\": true\r\n}"
     headers = {
     'authorization': "Basic YWRtaW5AYXBwLmFjdGl2aXRpLmNvbTphZG1pbg==",
     'content-type': "application/json",
     'cache-control': "no-cache",
     }
     j=0
    for j in range (0,i):
     appID=idarr[j]
     url = "http://34.203.167.72:8080/activiti-app/api/enterprise/app-definitions/"+appID+"/publish"
     response = requests.request("POST", url, data=payload, headers=headers)
     j+=1
     print(response.text)