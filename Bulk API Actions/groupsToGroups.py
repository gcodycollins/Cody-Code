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

addOrRemove = input("type 'add' to call POST method. Type 'remove' to call DELETE method :")

#Call POST if input is add
if (addOrRemove== 'add'):

    #API add group to group
    for i in range(0,100):
 
        # API 1 add groups to site test default sitecontributor group
        url = "http://34.205.72.40:8080/alfresco/service/api/groups/site_testacl_SiteContributor/children/GROUP_group"+str(i)

        headers = {
            'content-type': "application/json"
            }
        
        payload = "{\r\n\r\n}"

        response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth('admin','admin'))
        print(i)
        print(response.text)

#call DELETE if input is remove        
if (addOrRemove== 'remove'):

    #API remove group from group
    for i in range(0,100):
 
        # API 1 add groups to site test default sitecontributor group
        url = "http://34.205.72.40:8080/alfresco/service/api/groups/site_testacl_SiteContributor/children/GROUP_group"+str(i)

        headers = {
            'content-type': "application/json"
            }
        
        payload = "{\r\n\r\n}"

        response = requests.request("DELETE", url, headers=headers, data=payload, auth=HTTPBasicAuth('admin','admin'))
        print(i)
        print(response.text)