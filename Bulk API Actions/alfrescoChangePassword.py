import requests
from requests.auth import HTTPBasicAuth


users = ["test1", "test2", "test3"]

for i in range(0, len(users)):

    
    # API to update users' password
    url = "http://54.167.179.17:8080/alfresco/service/api/person/changepassword/"+users[i]

    headers = {
        'content-type': "application/json"
    }
            
    payload = "{\n\"newpw\":\"admin1\"\n}"
            
    response = requests.request("POST", url, data=payload, headers=headers, auth=HTTPBasicAuth('admin','admin'))
    
    print(response.text)