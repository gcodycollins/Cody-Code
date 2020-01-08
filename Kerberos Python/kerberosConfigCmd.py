##############################################
#
# Created by Grayson Cody Collins
#
# Please reach out to cody.collins@alfresco.com
# with any questions, improvements, or requests.
#
##############################################

##############################################
#
# This code is currently behind the gui counterpart. Please check gui
# version for up to date features and functions.
#
##############################################


import os, sys, shutil, fileinput, subprocess


#input for functionality
kerberosI = input("Implement Kerberos?\nyes to append kerberos configurations\nno to rollback global properties and share-config-custom to original\n")
krb5iniI=input("Create krb5.ini? yes or no\n")

activeDirectoryI =input("Create Service accounts, set SPNs, and generate Keytabs? yes or no\n")

input("This script assumes you have already correctly configured the DNS of your Alfresco server to correctly find the Kerberos server by FQDN. This script also assumes you have already installed Alfresco using the defaults in the easy installer and Alfresco can correctly start and run. This script also assumes Alfresco is NOT currently running\n\nPress Enter to continue...")



#input for parameters
pathI = input("Enter the Alfresco install directory: Ex. C:\Alfresco521\n")

if (kerberosI=="yes" or kerberosI=="y"):
    alfServerI = input("Enter the Alfresco server name: Ex. Cody-Alfresco\n")
    ldapFQDN=input("Enter the Fully Qualified Domain Name of the LDAP server: Ex. Controller.CodyKerberos.sso\n")
    ldapAdmin=input("Enter the username of an LDAP account that has user sync permissions(just username): Ex. Administrator\n")
    ldapAdminPass=input("Enter the password of the LDAP account with sync permissions.\n")
    ldapGroupBase=input("Enter the distinguishedName of the LDAP OU to sync groups from: Ex. OU=KerberosGroups,DC=CodyKerberos,DC=sso\n")
    ldapUserBase=input("Enter the distinguishedName of the LDAP OU to sync users from: Ex. OU=KerberosUsers,DC=CodyKerberos,DC=sso\n")
    keytabPath=input("Enter the path the Kerberos Keytabs are stored in: Ex. C:\etc\n")
    httpKeytabName=input("Enter the name for the HTTP keytab: Ex. alfrescohttp.keytab\n")
    cifsKeytabName=input("Enter the name for the cifs keytab: Ex. alfrescocifs.keytab\n")


    #strip domain from ldapFQDN
    start=ldapFQDN.find('.')+1
    domainI = ldapFQDN[start:]
    #domain I to uppercase for realm
    uDomainI = domainI.upper()
    #string text after period in domain for domainnetbios
    end=uDomainI.find('.')
    realm=uDomainI[0:end]




if (activeDirectoryI=="yes" or activeDirectoryI=="y"):
    cifsUserDN=input("Enter the full distinguishedName for the cifs service account: Ex. cn=alfrescocifs,cn=Users,dc=CodyKerberos,dc=sso\n")
    cifsPasswordI=input("Enter the password to use for the cifs service account.\n")
    httpUserDN=input("Enter the full distinguishedName for the HTTP service account: Ex. cn=alfrescohttp,cn=Users,dc=CodyKerberos,dc=sso\n")
    httpPasswordI=input("Enter the password to use for the HTTP service account.\n")
    
    #Strip the cifs username from the full cifsUserDN
    start=cifsUserDN.find('=')+1
    end=cifsUserDN.find(',')
    cifsUserName=cifsUserDN[start:end]

    #Strip the http username from the full httpUserDN
    start=httpUserDN.find('=')+1
    end=httpUserDN.find(',')
    httpUserName=httpUserDN[start:end]








#If activeDirectoryI was chosen as yes, create the powershell file
if (activeDirectoryI=="yes" or activeDirectoryI=="y"):

    #blank out file first before writing.
    ps = open('powershellAD.ps1','w').close()

    #open file to write output to
    ps = open('powershellAD.ps1','a')
    
    ps.write(r'Write-Host "You will now be prompted to log in with a domain admin account. Use the full account name. EX Administrator@Domain.com. then Press any key to continue ..."')
    ps.write('\n') 
    ps.write(r'$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")')
    ps.write('\n\n')

    ps.write(r'#get credentials to use for authentication into all powershell commands')
    ps.write('\n')
    ps.write(r'$cred = get-credential')
    ps.write('\n\n')


    #write service account creation powershell comamnds to powershell file

    ps.write(r'#create the service accounts')
    ps.write('\n')
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock { dsadd user "'+httpUserDN+r'" -samid '+httpUserName+r' -upn '+httpUserName+r'@'+domainI+r' -fn '+httpUserName+r' -display '+httpUserName+r' -pwd '+httpPasswordI+r' -mustchpwd no -canchpwd no -pwdneverexpires yes} -credential $cred')
    ps.write('\n')
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock { dsadd user "'+cifsUserDN+r'" -samid '+cifsUserName+r' -upn '+cifsUserName+r'@'+domainI+r' -fn '+cifsUserName+r' -display '+cifsUserName+r' -pwd '+cifsPasswordI+r' -mustchpwd no -canchpwd no -pwdneverexpires yes} -credential $cred')
    ps.write('\n\n')

    #write SPN setting commands to powershell file
    ps.write(r'#set the spns on the created service accounts')
    ps.write('\n')
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {setspn -a HTTP/'+alfServerI+'.'+domainI+' '+httpUserName+r'} -credential $cred')
    ps.write('\n')
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {setspn -a HTTP/'+alfServerI+' '+httpUserName+r'} -credential $cred')
    ps.write('\n\n')
    
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {setspn -a cifs/'+alfServerI+'.'+domainI+' '+cifsUserName+r'} -credential $cred')
    ps.write('\n')    
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {setspn -a cifs/'+alfServerI+' '+cifsUserName+r'} -credential $cred')
    ps.write('\n\n') 
    
    ps.write(r'Write-Host "Go enable delegation on the kerberos accounts, then Press any key to continue ..."')
    ps.write('\n') 
    ps.write(r'$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")')
    ps.write('\n\n')
    
    #write keytabs generation command to powershell file
    ps.write(r'#generate the keytabs and pull them back to the Alfresco server')
    ps.write('\n')
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock { md '+keytabPath+r'} -credential $cred')
    ps.write('\n\n')
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock { ktpass -princ HTTP/'+alfServerI+r'@'+uDomainI+r' -pass '+httpPasswordI+' -mapuser '+realm+'\\'+httpUserName+r' -crypto RC4-HMAC-NT -ptype KRB5_NT_PRINCIPAL -out '+keytabPath+'\\'+httpKeytabName+r' -kvno 0} -credential $cred')
    ps.write('\n\n')
    ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock { ktpass -princ cifs/'+alfServerI+r'@'+uDomainI+r' -pass '+cifsPasswordI+' -mapuser '+realm+'\\'+cifsUserName+r' -crypto RC4-HMAC-NT -ptype KRB5_NT_PRINCIPAL -out '+keytabPath+'\\'+cifsKeytabName+r' -kvno 0} -credential $cred')
    ps.write('\n\n')
    ps.write(r'$SourceSession = New-PSSession -ComputerName '+ldapFQDN+r' -credential $cred')
    ps.write('\n\n')
    ps.write(r'Copy-Item -FromSession $SourceSession -Path "'+keytabPath+r'" -Destination "C:\" -Recurse')

    ps.close()
    
    # get the current working directory to find the powershell file
    cwd = os.getcwd()

    p = subprocess.Popen(["powershell.exe", cwd+r"\powershellAD.ps1"], stdout=sys.stdout)
    p.communicate()
    




#create krb5.ini
if (krb5iniI=="yes" or krb5iniI=="y"):

    krb5iniPath=r'C:\Windows'
    krb5iniFile=r'krb5.ini'

    with open(os.path.join(krb5iniPath, krb5iniFile), 'w') as k5:
    
    
        k5.write(r'[logging]')
        k5.write('\n')
        k5.write(r' default = FILE:C:\Windows\krb5libs.log')
        k5.write('\n')        
        k5.write(r' kdc = FILE:C:\Windows\krb5kdc.log')
        k5.write('\n')        
        k5.write(r' admin_server = FILE:C:\Windows\kadmind.log')
        k5.write('\n\n')
        
        k5.write(r'[libdefaults]')
        k5.write('\n')        
        k5.write(r' default_realm = '+uDomainI+'')
        k5.write('\n')        
        k5.write(r' dns_lookup_realm = true')
        k5.write('\n')        
        k5.write(r' dns_lookup_kdc = true')
        k5.write('\n') 
        k5.write(r' ticket_lifetime = 24h')
        k5.write('\n') 
        k5.write(r' renew_lifetime = 7d')
        k5.write('\n') 
        k5.write(r' forwardable = true')
        k5.write('\n') 
        k5.write(r' default_tkt_enctypes = rc4-hmac')
        k5.write('\n') 
        k5.write(r' default_tgs_enctypes = rc4-hmac')
        k5.write('\n\n') 

        k5.write(r'[realms]')
        k5.write('\n') 
        k5.write(r' '+uDomainI+r' = {')
        k5.write('\n') 
        k5.write(r'  kdc = '+ldapFQDN)
        k5.write('\n') 
        k5.write(r'  admin_server = '+ldapFQDN)
        k5.write('\n') 
        k5.write(r' }')
 
        k5.close()

    
    

if (kerberosI=="yes" or kerberosI=="y"):


    #copy the current global properties file and append the kerberos and LDAP properties to the end of the active configuraiton file
    #also modify share.host and alfresco.host

    gloPropsSource=pathI+r'\tomcat\shared\classes\alfresco-global.properties'
    gloPropsOriginalCopy=pathI+r'\tomcat\shared\classes\alfresco-global.properties.original'

    shutil.copy(gloPropsSource, gloPropsOriginalCopy)

    alfrescoHost = 'alfresco.host='+alfServerI+'.'+domainI+''
    shareHost = 'share.host='+alfServerI+'.'+domainI+''



    with open(gloPropsOriginalCopy) as inF0, open(gloPropsSource, 'w') as outF0:
        for line in inF0:
        
            if (r'alfresco.host=' in line):
                line = alfrescoHost
                outF0.write(line+'\n')
                
            elif (r'share.host=' in line):
                line = shareHost
                outF0.write(line+'\n')    
                
            else:
                outF0.write(line)
            
        inF0.close()
        outF0.close()




    with open(gloPropsSource, 'a') as f0:
        f0.write('\n\n\n\n\n###KERB###')
        
        f0.write('\n\nkerberos.authentication.realm='+uDomainI+'')
        f0.write('\nkerberos.authentication.authenticateCIFS=false')
        f0.write('\nkerberos.authentication.sso.enabled=true')
        f0.write('\nkerberos.authentication.http.password='+httpPasswordI+'')
        f0.write('\nkerberos.authentication.stripUsernameSuffix=true')
        f0.write('\nkerberos.authentication.browser.ticketLogons=true')

        f0.write('\n\n\n\n\n###LDAP###')
        f0.write('\n\nauthentication.chain=kerberos1:kerberos,alfrescoNtlm1:alfrescoNtlm')
        f0.write('\nldap.authentication.active=true')
        f0.write('\nldap.authentication.allowGuestLogin=false')
        f0.write('\nldap.authentication.userNameFormat=%s@'+domainI+'')
        f0.write('\nldap.authentication.java.naming.provider.url=ldap://'+ldapFQDN+':389')
        f0.write('\nldap.synchronization.java.naming.security.principal='+ldapAdmin+'@'+domainI+'')
        f0.write('\nldap.synchronization.java.naming.security.credentials='+ldapAdminPass+'')
        f0.write('\nldap.synchronization.groupSearchBase='+ldapGroupBase)
        f0.write('\nldap.synchronization.userSearchBase='+ldapUserBase)
        f0.write('\nsynchronization.syncOnStartup=true')
        f0.write('\nsynchronization.allowDeletions=false')
        f0.write('\nsynchronization.synchronizeChangesOnly=false')
        f0.write('\nldap.synchronization.userIdAttributeName=sAMAccountName')
        f0.write('\nldap.synchronization.personQuery=(objectClass\=user)')
        f0.write('\nldap.synchronization.groupQuery=(objectClass\=group)')
        
        f0.close()




    #copy the current share-config-custom.xml and modify the active cofiguration

    shareConfigSource=pathI+r'\tomcat\shared\classes\alfresco\web-extension\share-config-custom.xml'
    shareConfigOriginalCopy=pathI+r'\tomcat\shared\classes\alfresco\web-extension\share-config-custom.xml.original'

    shutil.copy(shareConfigSource, shareConfigOriginalCopy)

    kerbPassword = r'         <password>'+httpPasswordI+r'</password>'
    kerbRealm = r'         <realm>'+uDomainI+'</realm>'
    kerbSpn=r'         <endpoint-spn>HTTP/'+alfServerI+'@'+uDomainI+'</endpoint-spn>'


    with open(shareConfigOriginalCopy) as inF1, open(shareConfigSource, 'w') as outF1:
        for line in inF1:
        
            if (r'condition="KerberosDisabled"' in line):
                line = r'   <config evaluator="string-compare" condition="Kerberos" replace="true">'
                outF1.write(line+'\n')
                
            elif (r'<password>' in line):
                line = kerbPassword
                outF1.write(line+'\n') 

            elif (r'</realm>' in line):
                line = kerbRealm
                outF1.write(line+'\n')

            elif (r'<endpoint-spn>' in line):
                line = kerbSpn
                outF1.write(line+'\n')

            elif (r'<!-- For production environment set verify-hostname to true.-->' in line):
                line = r'   <!-- For production environment set verify-hostname to true.-->'
                outF1.write(line+'\n')
                outF1.write('\n')
                

                outF1.write(r'    <config evaluator="string-compare" condition="Remote">')
                outF1.write('\n')
                outF1.write(r'      <remote>')
                outF1.write('\n')
                outF1.write(r'         <ssl-config>')
                outF1.write('\n')
                outF1.write(r'            <keystore-path>alfresco/web-extension/alfresco-system.p12</keystore-path>')
                outF1.write('\n')
                outF1.write(r'            <keystore-type>pkcs12</keystore-type>')
                outF1.write('\n')
                outF1.write(r'            <keystore-password>alfresco-system</keystore-password>')
                outF1.write('\n')

                outF1.write('\n')

                outF1.write(r'            <truststore-path>alfresco/web-extension/ssl-truststore</truststore-path>')
                outF1.write('\n')
                outF1.write(r'            <truststore-type>JCEKS</truststore-type>')
                outF1.write('\n')
                outF1.write(r'            <truststore-password>password</truststore-password>')
                outF1.write('\n')

                outF1.write('\n')

                outF1.write(r'            <verify-hostname>true</verify-hostname>')
                outF1.write('\n')
                outF1.write(r'         </ssl-config>')
                outF1.write('\n')

                outF1.write('\n')

                outF1.write(r'         <connector>')
                outF1.write('\n')
                outF1.write(r'            <id>alfrescoCookie</id>')
                outF1.write('\n')
                outF1.write(r'            <name>Alfresco Connector</name>')
                outF1.write('\n')
                outF1.write(r'            <description>Connects to an Alfresco instance using cookie-based authentication</description>')
                outF1.write('\n')
                outF1.write(r'            <class>org.alfresco.web.site.servlet.SlingshotAlfrescoConnector</class>')
                outF1.write('\n')
                outF1.write(r'         </connector>')
                outF1.write('\n')

                outF1.write('\n')
             
                outF1.write(r'         <connector>')
                outF1.write('\n')
                outF1.write(r'            <id>alfrescoHeader</id>')
                outF1.write('\n')
                outF1.write(r'            <name>Alfresco Connector</name>')
                outF1.write('\n')
                outF1.write(r'            <description>Connects to an Alfresco instance using header and cookie-based authentication</description>')
                outF1.write('\n')
                outF1.write(r'            <class>org.alfresco.web.site.servlet.SlingshotAlfrescoConnector</class>')
                outF1.write('\n')
                outF1.write(r'            <userHeader>SsoUserHeader</userHeader>')
                outF1.write('\n')
                outF1.write(r'         </connector>')
                outF1.write('\n')

                outF1.write('\n')

                outF1.write(r'         <endpoint>')
                outF1.write('\n')
                outF1.write(r'            <id>alfresco</id>')
                outF1.write('\n')
                outF1.write(r'            <name>Alfresco - user access</name>')
                outF1.write('\n')
                outF1.write(r'            <description>Access to Alfresco Repository WebScripts that require user authentication</description>')
                outF1.write('\n')
                outF1.write(r'            <connector-id>alfrescoCookie</connector-id>')
                outF1.write('\n')
                outF1.write(r'            <endpoint-url>http://localhost:8080/alfresco/wcs</endpoint-url>')
                outF1.write('\n')
                outF1.write(r'            <identity>user</identity>')
                outF1.write('\n')
                outF1.write(r'            <external-auth>true</external-auth>')
                outF1.write('\n')
                outF1.write(r'         </endpoint>')
                outF1.write('\n')

                outF1.write('\n')
             
                outF1.write(r'         <endpoint>')
                outF1.write('\n')
                outF1.write(r'            <id>alfresco-feed</id>')
                outF1.write('\n')
                outF1.write(r'            <parent-id>alfresco</parent-id>')
                outF1.write('\n')
                outF1.write(r'            <name>Alfresco Feed</name>')
                outF1.write('\n')
                outF1.write(r'            <description>Alfresco Feed - supports basic HTTP authentication via the EndPointProxyServlet</description>') 
                outF1.write('\n')
                outF1.write(r'            <connector-id>alfrescoHeader</connector-id> ')
                outF1.write('\n')
                outF1.write(r'            <endpoint-url>http://localhost:8080/alfresco/wcs</endpoint-url>')
                outF1.write('\n')
                outF1.write(r'            <identity>user</identity>')
                outF1.write('\n')
                outF1.write(r'            <external-auth>true</external-auth>')
                outF1.write('\n')
                outF1.write(r'         </endpoint>')
                outF1.write('\n')

                outF1.write('\n')
             
                outF1.write(r'         <endpoint>')
                outF1.write('\n')
                outF1.write(r'            <id>alfresco-api</id>')
                outF1.write('\n')
                outF1.write(r'            <parent-id>alfresco</parent-id>')
                outF1.write('\n')
                outF1.write(r'            <name>Alfresco Public API - user access</name>')
                outF1.write('\n')
                outF1.write(r'            <description>Access to Alfresco Repository Public API that require user authentication.')
                outF1.write('\n')
                outF1.write(r'                         This makes use of the authentication that is provided by parent \'alfresco\' endpoint.</description>')
                outF1.write('\n')
                outF1.write(r'            <connector-id>alfrescoHeader</connector-id>')
                outF1.write('\n')
                outF1.write(r'            <endpoint-url>http://localhost:8080/alfresco/api</endpoint-url>')
                outF1.write('\n')
                outF1.write(r'            <identity>user</identity>')
                outF1.write('\n')
                outF1.write(r'            <external-auth>true</external-auth>')
                outF1.write('\n')
                outF1.write(r'         </endpoint>')
                outF1.write('\n')
                outF1.write(r'      </remote>')
                outF1.write('\n')
                outF1.write(r'   </config>')
                outF1.write('\n')
                
                
            else:
                outF1.write(line)
            
        inF1.close()
        outF1.close()
        
        
        

    #modify the java.security to point to the java.login.config


    originalLoginConfigUrl=r'#login.config.url.1=file:${user.home}/.java.login.config'
    updatedLoginConfigUrl=r'login.config.url.1=file:${java.home}/lib/security/java.login.config'


    javaSecuritySource=pathI+r'\java\lib\security\java.security'
    javaSecurityOriginalCopy=pathI+r'\java\lib\security\java.security.original'

    shutil.copy(javaSecuritySource, javaSecurityOriginalCopy)


    with open(javaSecurityOriginalCopy) as inF2, open(javaSecuritySource, 'w') as outF2:
        for line in inF2:
        
            if (r'login.config.url.1' in line):
                line = updatedLoginConfigUrl
                outF2.write(line)
                
            else:
                outF2.write(line)
            
        inF2.close()
        outF2.close()
        
        
        
        
        
    #Create the java.login.config and populate

    javaLoginConfigPath=pathI+r'\java\lib\security'
    javaLoginConfigFile=r'java.login.config'

    with open(os.path.join(javaLoginConfigPath, javaLoginConfigFile), 'w') as f3:
        
        f3.write('Alfresco {')
        f3.write('\ncom.sun.security.auth.module.Krb5LoginModule sufficient;')
        f3.write('\n};')

        f3.write('\n\nAlfrescoCIFS {')
        f3.write('\ncom.sun.security.auth.module.Krb5LoginModule required')
        f3.write('\nstoreKey=true')
        f3.write('\nuseKeyTab=true\n')
        f3.write(r'keyTab="'+keytabPath+'\\'+cifsKeytabName+r'"')
        f3.write('\nprincipal="cifs/'+alfServerI+'@'+uDomainI+'";')
        f3.write('\n};')

        f3.write('\n\nAlfrescoHTTP {')
        f3.write('\ncom.sun.security.auth.module.Krb5LoginModule required')
        f3.write('\nstoreKey=true')
        f3.write('\nuseKeyTab=true\n')
        f3.write(r'keyTab="'+keytabPath+'\\'+httpKeytabName+r'"')
        f3.write('\nprincipal="HTTP/'+alfServerI+'@'+uDomainI+'";')
        f3.write('\n};')

        f3.write('\n\nShareHTTP {')
        f3.write('\ncom.sun.security.auth.module.Krb5LoginModule required')
        f3.write('\nstoreKey=true')
        f3.write('\nuseKeyTab=true\n')
        f3.write(r'keyTab="'+keytabPath+'\\'+httpKeytabName+r'"')
        f3.write('\nprincipal="HTTP/'+alfServerI+'@'+uDomainI+'";')
        f3.write('\n};')

        f3.write('\n\ncom.sun.net.ssl.client {')
        f3.write('\ncom.sun.security.auth.module.Krb5LoginModule sufficient;')
        f3.write('\n};')

        f3.write('\n\nother {')
        f3.write('\ncom.sun.security.auth.module.Krb5LoginModule sufficient;')
        f3.write('\n};')
        
        
        f3.close()
        
        
        
        
elif (kerberosI=="no" or kerberosI=="n"):

    gloPropsCurrent=pathI+r'\tomcat\shared\classes\alfresco-global.properties'
    gloPropsOriginalCopy=pathI+r'\tomcat\shared\classes\alfresco-global.properties.original'

    
    shutil.copy(gloPropsOriginalCopy, gloPropsCurrent)
    
    os.remove(gloPropsOriginalCopy)
    
    
    
    shareConfigCurrent=pathI+r'\tomcat\shared\classes\alfresco\web-extension\share-config-custom.xml'
    shareConfigOriginalCopy=pathI+r'\tomcat\shared\classes\alfresco\web-extension\share-config-custom.xml.original'

    
    shutil.copy(shareConfigOriginalCopy, shareConfigCurrent)
    
    os.remove(shareConfigOriginalCopy)
    
    
    
    javaSecurityCurrent=pathI+r'\java\lib\security\java.security'
    javaSecurityOriginalCopy=pathI+r'\java\lib\security\java.security.original'
    
    shutil.copy(javaSecurityOriginalCopy, javaSecurityCurrent)
    
    os.remove(javaSecurityOriginalCopy)
    
    
    
    javaLoginConfigPath=pathI+r'\java\lib\security\java.login.config'
    
    os.remove(javaLoginConfigPath)