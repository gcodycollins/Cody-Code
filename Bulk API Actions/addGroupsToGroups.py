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
import time


#API add group to group
for i in range(0,1000):
 
    # API 1 create groups
    url = "http://34.205.72.40:8080/alfresco/service/api/groups/site_test_SiteContributor/children/GROUP_group"+str(i)

    headers = {
        'content-type': "application/json"
        }
        
    payload = "{\r\n\r\n}"

    response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth('admin','admin'))

    print(response.text)
