import requests
from requests.auth import HTTPBasicAuth
import json
import time


#API add group to group
for i in range(0,1800):
 
    # API 1 create groups
    url = "http://34.203.167.72:8080/activiti-app/api/enterprise/process-instances"

    headers = {
        'content-type': "application/json"
        }
        
    payload = "{\r\n\"processDefinitionId\": \"load50var:2:56\",\r\n\"businessKey\" : \"load 50 var\",\r\n\"values\" : {\r\n\t\"label\":\"label\",\r\n\t\"label1\":\"label1\",\r\n\t\"label2\":\"label2\",\r\n\t\"label3\":\"label3\",\r\n\t\"label4\":\"label4\",\r\n\t\"label5\":\"label5\",\r\n\t\"label6\":\"label6\",\r\n\t\"label7\":\"label7\",\r\n\t\"label8\":\"label8\",\r\n\t\"label9\":\"label9\",\r\n\t\"label10\":\"label10\",\r\n\t\"label11\":\"label11\",\r\n\t\"label12\":\"label12\",\r\n\t\"label13\":\"label13\",\r\n\t\"label14\":\"label14\",\r\n\t\"label15\":\"label15\",\r\n\t\"label16\":\"label16\",\r\n\t\"label17\":\"label17\",\r\n\t\"label18\":\"label18\",\r\n\t\"label19\":\"label19\",\r\n\t\"label20\":\"label20\",\r\n\t\"label21\":\"label21\",\r\n\t\"label22\":\"label22\",\r\n\t\"label23\":\"label23\",\r\n\t\"label24\":\"label24\",\r\n\t\"label25\":\"label25\",\r\n\t\"label26\":\"label26\",\r\n\t\"label27\":\"label27\",\r\n\t\"label28\":\"label28\",\r\n\t\"label29\":\"label29\",\r\n\t\"label30\":\"label30\",\r\n\t\"label31\":\"label31\",\r\n\t\"label32\":\"label32\",\r\n\t\"label33\":\"label33\",\r\n\t\"label34\":\"label34\",\r\n\t\"label35\":\"label35\",\r\n\t\"label36\":\"label36\",\r\n\t\"label37\":\"label37\",\r\n\t\"label38\":\"label38\",\r\n\t\"label39\":\"label39\",\r\n\t\"label40\":\"label40\",\r\n\t\"label41\":\"label41\",\r\n\t\"label42\":\"label42\",\r\n\t\"label43\":\"label43\",\r\n\t\"label44\":\"label44\",\r\n\t\"label45\":\"label45\",\r\n\t\"label46\":\"label46\",\r\n\t\"label47\":\"label47\",\r\n\t\"label48\":\"label48\",\r\n\t\"label49\":\"label49\"\r\n}\r\n}"

    response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

    print(response.text)
