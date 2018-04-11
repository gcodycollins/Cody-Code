'''
Contact:
 Created by Grayson Cody Collins
 Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3 with any questions, improvements, or requests.

Purpose:
 The Function of this code is to gather APS configurations and statistics.

Wishlist/future feature tracker for my own personal memory:
 -SQL code execution against configured DB, DB vendor specific SQL based on pulled properties.
 -When pulling certain properties, logic to go and get other files to get related configs.
 -Logic to pre-emptively inform customer for recommendation? Or do all of that on our end?
 -Logic to handle if the DB url contains variables like ${dbName}. Retrieve those variables too.
 -Handle multiple of the same properties, only read the last logged one just like in spring.
 
Assumptions/Other:
 -This code was developed and tested using Python 3 branch.
 -For DB vendors, ensure that necessary steps for each version are followed.
  -Oracle: Download cx_Oracle Package from https://oracle.github.io/python-cx_Oracle/

'''
#Imports
import os
import glob
import cx_Oracle

from datetime import datetime
    
    
    
    
    
    
    
    
    
####################### 
###   Definitions   ###
#######################

#find specific files in (hopefully) the correct APS directory
def findFile(pattern):


    print("Searching for file matching "+pattern)
    result = glob.glob(pattern, recursive=True)

    return result;
    
    
    
    
    
#Source: http://opensourceforu.com/2016/10/file-search-with-python/
#Used for Windows to get all current drives. In case APS is on D: or other non-C: drive 
def get_drives():
    response = os.popen("wmic logicaldisk get caption")
    list1 = []
    total_file = []
    t1= datetime.now()
    for line in response.readlines():
        line = line.strip("\n")
        line = line.strip("\r")
        line = line.strip(" ")
        line = line.strip("'")
        if (line == "Caption" or line == ""):
            continue
        list1.append(line)
    return list1
    
    
    

    
#New Def
    
#######################   
### End Definitions ###
#######################










#Check if Windows
if os.name =='nt':
    windows=True

#Execute if Windows    
if windows:

    #get all drive letters
    drives= get_drives()

    results=[]
    
    for drive in drives:
        results += findFile(drive+'/**/tomcat/lib/activiti-app.properties')
     
    #handle if there is more than one possible APS environment found
    if (len(results)>1):
    
        print("\n\nMore than one possible APS Environment found.\n")
        
        for i in range (0,len(results)):
            
            print (str(i)+": "+results[i])
        
        #prompt for user input of correct path choice
        envChoice= input("\nEnter number of correct APS: ")
        
        #set variable equal to chosen file
        actAppProp=results[int(envChoice)]
        
    #else for if just one result of activiti-app.properties found    
    else:
    
        actAppProp=results[0]
        



        
    #Declare default values for properties
    datasourceDriver="datasource.driver="
    datasourceUrl="datasource.url="
    datasourceUsername="datasource.username="
    datasourcePassword="datasource.password="
    hibernateDialect="hibernate.dialect="
        
    #Open the found activiti-app.properties file
    with open(actAppProp) as appProp:
    
        print("Reading File: "+actAppProp)
    
        #parse the file line by line. This also ensures that when the same property is uncommented, it will always pick up the 
        #last uncommented property just like spring does
        for line in appProp:
        
            #Pull DB Properties.          
            if (r'datasource.driver=' in line and not "#" in line):
                datasourceDriver=line
                
            elif(r'datasource.url=' in line and not "#" in line):
                datasourceUrl=line
                
            elif(r'datasource.username=' in line and not "#" in line):
                datasourceUsername=line
                
            elif(r'datasource.password=' in line and not "#" in line):
                datasourcePassword=line
                
            elif(r'hibernate.dialect=' in line and not "#" in line):
                hibernateDialect=line
                
        appProp.close()
        print("Read Complete\n")
                
                
    
    
    #Open file to begin writing all useful HC information to
    #blank out file first before writing.
    HC = open('HCInfo.txt','w').close()
    #open file to write output to
    HC = open('HCInfo.txt','w')
    
    print("Writing File: HCInfo.txt")
    
    #Write HC file with pre filled properties to account for when multiple are found.
    HC.write('###########################\n### Database Properties ###\n###########################\n\n')
    HC.write(datasourceDriver)
    HC.write(datasourceUrl)
    HC.write(datasourceUsername)
    #TODO change this so it doesn't print out plain text DB password
    HC.write(datasourcePassword)
    HC.write(hibernateDialect)
    
    print("Write Complete\n")
    
    print("Executing Database Queries:")
    
    HC.write('\n\n############################\n### Database Table Count ###\n############################\n\n')
    
    #Make Database Connection using previously gathered connection
    
    #Strip the property names from each string variable
    databaseUsername=datasourceUsername.replace("datasource.username=","")
    databaseUsername= databaseUsername.replace("\n","")
    databasePassword=datasourcePassword.replace("datasource.password=","")
    databasePassword=databasePassword.replace("\n","")
    
    #get db port, url, and name by splitting datasourceUrl
    dbConnection=datasourceUrl.split(":")
    
    databaseURL=dbConnection[3]
    databaseURL=databaseURL.replace("@","")
    databasePort=dbConnection[4]
    databaseName=dbConnection[5]
    databaseName=databaseName.replace("\n","")
    
    dbURL=databaseURL+":"+databasePort+"/"+databaseName
    
    #Sources: http://cx-oracle.readthedocs.io/en/latest/installation.html , https://support.esri.com/en/technical-article/000011659
    #Check for DB vendor
    
    #if Oracle DB
    if (hibernateDialect=='hibernate.dialect=org.hibernate.dialect.Oracle10gDialect'):
        
        
        
        #for ACT_EVT_LOG
        print("--Executing Query: SELECT count(*) FROM "+databaseUsername+".ACT_EVT_LOG;")
        
        #DB connection and query
        connection = cx_Oracle.connect(databaseUsername, databasePassword, dbURL)
        cursor=connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM """+databaseUsername+""".ACT_EVT_LOG""")
            
        #get Count from query
        response=""
        for result in cursor:
            response+=str(result)
        
        response=response.replace("(","").replace(",","").replace(")","")
        print("--Query Execution Complete\n")
        
        HC.write("ACT_EVT_LOG:\r")
        HC.write("Count= "+response+"\n\n")
        
        
        
        #for PROCESSED_ACTIVITI_EVENTS
        print("--Executing Query: SELECT count(*) FROM "+databaseUsername+".PROCESSED_ACTIVITI_EVENTS;")
        
        #DB connection and query
        connection = cx_Oracle.connect(databaseUsername, databasePassword, dbURL)
        cursor=connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM """+databaseUsername+""".PROCESSED_ACTIVITI_EVENTS""")
            
        #get Count from query
        response=""
        for result in cursor:
            response+=str(result)
        
        response=response.replace("(","").replace(",","").replace(")","")
        print("--Query Execution Complete\n")
        
        HC.write("PROCESSED_ACTIVITI_EVENTS:\r")
        HC.write("Count= "+response+"\n\n")
        
        
        
        #for ACT_HI_PROCINST
        print("--Executing Query: SELECT count(*) FROM "+databaseUsername+".ACT_HI_PROCINST;")
        
        #DB connection and query
        connection = cx_Oracle.connect(databaseUsername, databasePassword, dbURL)
        cursor=connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM """+databaseUsername+""".ACT_HI_PROCINST""")
            
        #get Count from query
        response=""
        for result in cursor:
            response+=str(result)
        
        response=response.replace("(","").replace(",","").replace(")","")
        print("--Query Execution Complete\n")
        
        HC.write("ACT_HI_PROCINST:\r")
        HC.write("Count= "+response+"\n\n")
        
        
        
        #for ACT_HI_TASKINST
        print("--Executing Query: SELECT count(*) FROM "+databaseUsername+".ACT_HI_TASKINST;")
        
        #DB connection and query
        connection = cx_Oracle.connect(databaseUsername, databasePassword, dbURL)
        cursor=connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM """+databaseUsername+""".ACT_HI_TASKINST""")
            
        #get Count from query
        response=""
        for result in cursor:
            response+=str(result)
        
        response=response.replace("(","").replace(",","").replace(")","")
        print("--Query Execution Complete\n")
        
        HC.write("ACT_HI_TASKINST:\r")
        HC.write("Count= "+response+"\n\n")
        
        
        
        #for ACT_HI_VARINST
        print("--Executing Query: SELECT count(*) FROM "+databaseUsername+".ACT_HI_VARINST;")
        
        #DB connection and query
        connection = cx_Oracle.connect(databaseUsername, databasePassword, dbURL)
        cursor=connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM """+databaseUsername+""".ACT_HI_VARINST""")
            
        #get Count from query
        response=""
        for result in cursor:
            response+=str(result)
        
        response=response.replace("(","").replace(",","").replace(")","")
        print("--Query Execution Complete\n")
        
        HC.write("ACT_HI_VARINST:\r")
        HC.write("Count= "+response+"\n\n")
        
        
        
        #for ACT_RU_TASK
        print("--Executing Query: SELECT count(*) FROM "+databaseUsername+".ACT_RU_TASK;")
        
        #DB connection and query
        connection = cx_Oracle.connect(databaseUsername, databasePassword, dbURL)
        cursor=connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM """+databaseUsername+""".ACT_RU_TASK""")
            
        #get Count from query
        response=""
        for result in cursor:
            response+=str(result)
        
        response=response.replace("(","").replace(",","").replace(")","")
        print("--Query Execution Complete\n")
        
        HC.write("ACT_RU_TASK:\r")
        HC.write("Count= "+response+"\n\n")
        
        
        
        #for ACT_RU_VARIABLE
        print("--Executing Query: SELECT count(*) FROM "+databaseUsername+".ACT_RU_VARIABLE;")
        
        #DB connection and query
        connection = cx_Oracle.connect(databaseUsername, databasePassword, dbURL)
        cursor=connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM """+databaseUsername+""".ACT_RU_VARIABLE""")
            
        #get Count from query
        response=""
        for result in cursor:
            response+=str(result)
        
        response=response.replace("(","").replace(",","").replace(")","")
        print("--Query Execution Complete\n")
        
        HC.write("ACT_RU_VARIABLE:\r")
        HC.write("Count= "+response+"\n\n")
        
        
        print("Database Queries Complete")