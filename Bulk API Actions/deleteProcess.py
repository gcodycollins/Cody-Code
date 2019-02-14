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

##################
#NOTES:
#
#Running this one time will cancel in-flight processes and delete already completed or cancelled processes from the database.
#Run this twice to cancel and delete in-flight processes.
##################

#Declare array with processInstanceId
processInstanceIdArray=["84","90","96","102","108","114","120","126","132","78"]

#Loop through the array to make the API call with each processInstanceId
for i in range (0, len(processInstanceIdArray)):

    ################
    #Change APS URL#
    ################
    url0 = "http://localhost:8080/activiti-app/api/enterprise/process-instances/"+processInstanceIdArray[i]

    headers0 = {
        'content-type': "application/json"
        }

    ###############################
    #Change authentication details#
    ###############################
    response0 = requests.request("DELETE", url0, headers=headers0,auth=HTTPBasicAuth('admin@app.activiti.com','admin'))

    #debug 
    if response0.text=="":
        print("ProcessInstance "+processInstanceIdArray[i]+" Cancelled/Deleted Successfully")
    else:
        print(response0.text)