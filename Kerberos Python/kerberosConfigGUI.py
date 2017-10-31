from tkinter import *
import os, sys, shutil, fileinput, subprocess

class Application(Frame):



    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

        
        
    def create_widgets(self):
        #Label(self, text = "Select all that apply:").grid(row = 1, column = 0, sticky = W)
        
        self.checkBoxKerberosI = BooleanVar()
        self.kerberosI = Checkbutton(self,text = "Implement Kerberos Configurations in the Alfresco Directory?",variable = self.checkBoxKerberosI,command = self.Kerberos_Configuration)
        self.kerberosI.grid(row = 2, column = 0, sticky = W)


        self.checkBoxKerberosR = BooleanVar()
        self.kerberosR = Checkbutton(self, text = "Rollback Alfresco directory to original alfresco-global.properties and share-config-custom.xml?", variable = self.checkBoxKerberosR,command = self.Rollback_Original)
        self.kerberosR.grid(row = 30, column = 0, sticky = W)
        
        
        
        self.close_button = Button(self, text="Run", command=self.run)
        self.close_button.grid(row=50, column = 0, sticky =W)
        
        
        
        self.close_button = Button(self, text="Close", command=self.quit)
        self.close_button.grid(row=51, column =0, sticky =W)

        
        
    def Kerberos_Configuration(self):
        
        if self.checkBoxKerberosI.get():
            self.LabelDir= Label(self, text="Alfreco Install Directory: ")
            self.LabelDir.grid(row = 3, column =0, sticky = W)
            self.dir = Entry(self)
            self.dir.grid(row=3, column=0)
            
            self.LabelServerName= Label(self, text="Alfreco Server Name: ")
            self.LabelServerName.grid(row = 4, column =0, sticky = W)
            self.serverName = Entry(self)
            self.serverName.grid(row=4, column=0)
            
            self.LabelLdapFqdn= Label(self, text="LDAP Fully Qualified Domain Name: ")
            self.LabelLdapFqdn.grid(row = 5, column =0, sticky = W)
            self.ldapFqdn = Entry(self)
            self.ldapFqdn.grid(row=5, column=0)
            
            self.LabelAdminName= Label(self, text="LDAP Admin Name: ")
            self.LabelAdminName.grid(row = 6, column =0, sticky = W)
            self.adminName = Entry(self)
            self.adminName.grid(row=6, column=0)
            
            self.LabelAdminPass= Label(self, text="LDAP Admin Password: ")
            self.LabelAdminPass.grid(row = 7, column =0, sticky = W)
            self.adminPass = Entry(self)
            self.adminPass.grid(row=7, column=0)
            
            self.LabelGroupBase= Label(self, text="LDAP Group Search Base: ")
            self.LabelGroupBase.grid(row = 8, column =0, sticky = W)
            self.groupBase = Entry(self)
            self.groupBase.grid(row=8, column=0)
            
            self.LabelUserBase= Label(self, text="LDAP User Search Base: ")
            self.LabelUserBase.grid(row = 9, column =0, sticky = W)
            self.userBase = Entry(self)
            self.userBase.grid(row=9, column=0)
            
            self.LabelKeytabPath= Label(self, text="Keytab Path: ")
            self.LabelKeytabPath.grid(row = 10, column =0, sticky = W)
            self.keytabPath = Entry(self)
            self.keytabPath.grid(row=10, column=0)
            
            self.LabelHTTPKeytab= Label(self, text="HTTP Keytab Name: ")
            self.LabelHTTPKeytab.grid(row = 11, column =0, sticky = W)
            self.httpKeytab = Entry(self)
            self.httpKeytab.grid(row=11, column=0)       

            self.LabelCifsKeytab= Label(self, text="cifs Keytab Name: ")
            self.LabelCifsKeytab.grid(row = 12, column =0, sticky = W)
            self.cifsKeytab = Entry(self)
            self.cifsKeytab.grid(row=12, column=0)                
            
            
            
            self.checkBoxKrb5 = BooleanVar()
            self.krb5 = Checkbutton(self,text = "Create krb5.ini?",variable = self.checkBoxKrb5)
            self.krb5.grid(row = 13, column = 0, sticky = W)
            
            
            
            
            self.checkBoxAD = BooleanVar()
            self.aD = Checkbutton(self, text = "Create service accounts, set SPNs, and Generate Keytabs?", variable = self.checkBoxAD,command = self.Active_Directory)
            self.aD.grid(row = 20, column = 0, sticky = W)
            
            
            
            self.checkBoxKerberosR = BooleanVar()
            self.kerberosR = Checkbutton(self, text = "Rollback Alfresco directory to original alfresco-global.properties and share-config-custom.xml?", variable = self.checkBoxKerberosR,command = self.Rollback_Original, state=DISABLED)
            self.kerberosR.grid(row = 30, column = 0, sticky = W)
            
        else:
            self.LabelDir.grid_forget()
            self.dir.grid_forget()
            
            self.LabelServerName.grid_forget()
            self.serverName.grid_forget()
            
            self.LabelLdapFqdn.grid_forget()
            self.ldapFqdn.grid_forget()
            
            self.LabelAdminName.grid_forget()
            self.adminName.grid_forget()
            
            self.LabelAdminPass.grid_forget()
            self.adminPass.grid_forget()
            
            self.LabelGroupBase.grid_forget()
            self.groupBase.grid_forget()
            
            self.LabelUserBase.grid_forget()
            self.userBase.grid_forget()
            
            self.LabelKeytabPath.grid_forget()
            self.keytabPath.grid_forget()
            
            self.LabelHTTPKeytab.grid_forget()
            self.httpKeytab.grid_forget()
            
            self.LabelCifsKeytab.grid_forget()
            self.cifsKeytab.grid_forget()



            self.krb5.grid_forget()
            
            self.aD.grid_forget()
            
            
            
            self.checkBoxKerberosR = BooleanVar()
            self.kerberosR = Checkbutton(self, text = "Rollback Alfresco directory to original alfresco-global.properties and share-config-custom.xml?", variable = self.checkBoxKerberosR,command = self.Rollback_Original)
            self.kerberosR.grid(row = 30, column = 0, sticky = W)

           
            
    def Active_Directory(self):
            
        if self.checkBoxAD.get():
        
        
            self.LabelHTTPUserDN= Label(self, text="HTTP User DistinguishedName: ")
            self.LabelHTTPUserDN.grid(row = 21, column =0, sticky = W)
            self.httpUserDN = Entry(self)
            self.httpUserDN.grid(row=21, column=0)
            
            self.LabelHTTPUserPass= Label(self, text="HTTP User Password: ")
            self.LabelHTTPUserPass.grid(row = 22, column =0, sticky = W)
            self.httpUserPass = Entry(self)
            self.httpUserPass.grid(row=22, column=0)
            
            self.LabelcifsUserDN= Label(self, text="cifs User DistinguishedName: ")
            self.LabelcifsUserDN.grid(row = 23, column =0, sticky = W)
            self.cifsUserDN = Entry(self)
            self.cifsUserDN.grid(row=23, column=0)      

            self.LabelCifsUserPass= Label(self, text="cifs User Password: ")
            self.LabelCifsUserPass.grid(row = 24, column =0, sticky = W)
            self.cifsUserPass = Entry(self)
            self.cifsUserPass.grid(row=24, column=0) 
            
            self.LabelLdapAdminPS= Label(self, text="Enter LDAP Administrator Domain\\Username: ")
            self.LabelLdapAdminPS.grid(row = 25, column =0, sticky = W)
            self.ldapAdminPS = Entry(self)
            self.ldapAdminPS.grid(row=25, column=0)      

            self.LabelLdapPassPS= Label(self, text="Enter LDAP Administrator Password: ")
            self.LabelLdapPassPS.grid(row = 26, column =0, sticky = W)
            self.ldapPassPS = Entry(self)
            self.ldapPassPS.grid(row=26, column=0) 
            
            
        else:
        
            self.LabelHTTPUserDN.grid_forget()
            self.httpUserDN.grid_forget()
            
            self.LabelHTTPUserPass.grid_forget()
            self.httpUserPass.grid_forget()
            
            self.LabelcifsUserDN.grid_forget()
            self.cifsUserDN.grid_forget()
            
            self.LabelCifsUserPass.grid_forget()
            self.cifsUserPass.grid_forget()
            
            self.LabelLdapAdminPS.grid_forget()
            self.ldapAdminPS.grid_forget()
            
            self.LabelLdapPassPS.grid_forget()
            self.ldapPassPS.grid_forget()

            
        
    def Rollback_Original(self):
    
        if self.checkBoxKerberosR.get():   

            self.LabelDir= Label(self, text="Alfreco Install Directory: ")
            self.LabelDir.grid(row = 31, column =0, sticky = W)
            self.dir = Entry(self)
            self.dir.grid(row=31, column=0)      
            
            self.checkBoxKerberosI = BooleanVar()
            self.kerberosI = Checkbutton(self,text = "Implement Kerberos Configurations in the Alfresco Directory?",variable = self.checkBoxKerberosI, command = self.Kerberos_Configuration, state=DISABLED)
            self.kerberosI.grid(row = 2, column = 0, sticky = W)
            
            
        else:
        
            self.LabelDir.grid_forget()
            self.dir.grid_forget()
        
            self.checkBoxKerberosI = BooleanVar()
            self.kerberosI = Checkbutton(self,text = "Implement Kerberos Configurations in the Alfresco Directory?",variable = self.checkBoxKerberosI, command = self.Kerberos_Configuration)
            self.kerberosI.grid(row = 2, column = 0, sticky = W)
            
            
            
    def run(self):       
        
        
        
        #take the input and store it as variables
        pathI = self.dir.get()
        if (self.checkBoxKerberosR.get()==False):
            kerberosI=self.checkBoxKerberosI.get()
            krb5iniI= self.checkBoxKrb5.get()
            activeDirectoryI=self.checkBoxAD.get()
            
        elif (self.checkBoxKerberosR.get()==True):
        
            kerberosI=False
            krb5iniI=False
            activeDirectoryI=False

        if (kerberosI==True):
            alfServerI = self.serverName.get()
            ldapFQDN=self.ldapFqdn.get()
            ldapAdmin=self.adminName.get()
            ldapAdminPass=self.adminPass.get()
            ldapGroupBase=self.groupBase.get()
            ldapUserBase=self.userBase.get()
            keytabPath=self.keytabPath.get()
            httpKeytabName=self.httpKeytab.get()
            cifsKeytabName=self.cifsKeytab.get()


            #strip domain from ldapFQDN
            start=ldapFQDN.find('.')+1
            domainI = ldapFQDN[start:]
            #domain I to uppercase for realm
            uDomainI = domainI.upper()
            #string text after period in domain for domainnetbios
            end=uDomainI.find('.')
            realm=uDomainI[0:end]




        if (activeDirectoryI==True):

            httpUserDN=self.httpUserDN.get()
            httpPasswordI=self.httpUserPass.get()
            cifsUserDN=self.cifsUserDN.get()
            cifsPasswordI=self.cifsUserPass.get()
            psAdmin = self.ldapAdminPS.get()
            psPass = self.ldapPassPS.get()
            
            #Strip the cifs username from the full cifsUserDN
            start=cifsUserDN.find('=')+1
            end=cifsUserDN.find(',')
            cifsUserName=cifsUserDN[start:end]

            #Strip the http username from the full httpUserDN
            start=httpUserDN.find('=')+1
            end=httpUserDN.find(',')
            httpUserName=httpUserDN[start:end]


            #blank out file first before writing.
            ps = open('powershellAD.ps1','w').close()

            #open file to write output to
            ps = open('powershellAD.ps1','a')

            #write to the powershell file the admin username and password
            ps.write(r"#pass the domain admin and username to credentials to be used for subsequent calls.")
            ps.write('\n')
            ps.write(r'$User = "'+psAdmin+'"')
            ps.write('\n')


            ps.write(r'$PWord = ConvertTo-SecureString -String "'+psPass+'" -AsPlainText -Force')
            ps.write('\n')

            
            ps.write(r'$cred = New-Object -TypeName "System.Management.Automation.PSCredential" -ArgumentList $User, $PWord')
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
            
            #write delegation generating comamnds to powershell
            ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {powershell "Set-ADAccountControl -Identity '+httpUserName+r' -TrustedForDelegation 1 -TrustedToAuthForDelegation 0"} -credential $cred')
            ps.write('\n')    
            ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {powershell "Set-ADAccountControl -Identity '+cifsUserName+r' -DoesNotRequirePreAuth 1 -TrustedForDelegation 1 -TrustedToAuthForDelegation 0"} -credential $cred')
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
        if (krb5iniI==True):

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

            
            

        if (kerberosI==True):


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
                
                
                
                
        elif (kerberosI==False):

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
      

root = Tk()
root.title("Kerberos Configurer")
app = Application(root)
root.mainloop()