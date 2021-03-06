'''

##########################################################################################################################################
#
# Created by Cody Collins
#
# Please reach out to cody.collins@alfresco.com
#
##########################################################################################################################################

##########################################################################################################################################
#
# The function of this code is to provide a GUI tool that can be used to configure
# Kerberos settings in both an APS and ACS directory. Currently, this is only supported
# on a Windows Applicaiton server and Windows Active Directory system.
#
# Some assumptions include that the APC and ACS environment this is run against is an 
# installer created environment. This is because hardcoded paths to the configuration files are used
# and those hardcoded paths are based off of an environment created by the installer.
#
# This code also assumes that you have configured the correct DNS for the Kerberos environment.
# This code also assumes that you have correctly implemented the client level configuration on
# the end user client machine.
#
##########################################################################################################################################

##########################################################################################################################################
#
#Wishlist/future feature tracker for my own personal memory:
#
# DONE 2.0- Option to Hide ACS/APS options to save screen real-estate.
# DONE 2.0- Separate run buttons for ACS and APS. No more confusing hidden checkboxes.
# DONE 2.0- Changing rollbacks from checkbox to its own separate button.
# DONE 2.0- Data persistence in the label fields if items are unchecked and later checked again.
# DONE 2.0- Change options to not hide and then display but to grey out options.
# DONE 2.0- Modifying GUI to show all data. Currently it cuts off text from long input
# DONE 2.0- Random password generator button. Populates password fields.
# DONE 2.0- Noticiations in Python Gui when action is complete.
# DONE 2.0- Read from file, button to pull properties in from file and populate UI.
#
# Automated kinit keytab checker. If it doesn't get a ticket, let the UI know.
# Find property files, don't just use hard coded values.
# When clicking close, save all current fields to file. On next restart, pull those values.
#
##########################################################################################################################################

'''

#!/bin/python3

from tkinter import *
import os, sys, shutil, fileinput, subprocess
import random



class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

        
        
        
        
        
        
        
        
        
    #main screen declaration with all options enabled    
    def create_widgets(self):
    
        #Alfresco Content Services Implement
        self.LabelACS= Label(self, text = "Alfresco Content Services")
        self.LabelACS.grid(row = 1, column = 0, sticky = W)
        
        self.toggleACS = Button(self, text = "Toggle APS", command = self.toggleACS)
        self.toggleACS.grid(row = 1, column = 0)
        
        self.LabelDir= Label(self, text="Alfreco (ACS) Install Directory: ")
        self.LabelDir.grid(row = 3, column =0, sticky = W)
        self.dir = Entry(self, width=100)
        self.dir.grid(row=4, column=0, sticky =W)
            
        self.LabelServerName= Label(self, text="Alfresco Server Name: ")
        self.LabelServerName.grid(row = 5, column =0, sticky = W)
        self.serverName = Entry(self, width=100)
        self.serverName.grid(row=6, column=0, sticky=W)
            
        self.LabelLdapFqdn= Label(self, text="LDAP Fully Qualified Domain Name: ")
        self.LabelLdapFqdn.grid(row = 7, column =0, sticky = W)
        self.ldapFqdn = Entry(self, width=100)
        self.ldapFqdn.grid(row=8, column=0, sticky=W)
            
        self.LabelAdminName= Label(self, text="LDAP Admin Name: ")
        self.LabelAdminName.grid(row = 9, column =0, sticky = W)
        self.adminName = Entry(self, width=100)
        self.adminName.grid(row=10, column=0, sticky=W)
            
        self.LabelAdminPass= Label(self, text="LDAP Admin Password: ")
        self.LabelAdminPass.grid(row = 11, column =0, sticky = W)
        self.adminPass = Entry(self, width=100)
        self.adminPass.grid(row=12, column=0, sticky=W)
            
        self.LabelGroupBase= Label(self, text="LDAP Group Search Base: ")
        self.LabelGroupBase.grid(row = 13, column =0, sticky = W)
        self.groupBase = Entry(self, width=100)
        self.groupBase.grid(row=14, column=0, sticky=W)
            
        self.LabelUserBase= Label(self, text="LDAP User Search Base: ")
        self.LabelUserBase.grid(row = 15, column =0, sticky = W)
        self.userBase = Entry(self,width=100)
        self.userBase.grid(row=16, column=0, sticky=W)
            
        self.LabelKeytabPath= Label(self, text="Keytab Path: ")
        self.LabelKeytabPath.grid(row = 17, column =0, sticky = W)
        self.keytabPath = Entry(self, width=100)
        self.keytabPath.grid(row=18, column=0, sticky=W)
           
        self.LabelHTTPKeytab= Label(self, text="HTTP Keytab Name: ")
        self.LabelHTTPKeytab.grid(row = 19, column =0, sticky = W)
        self.httpKeytab = Entry(self, width=100)
        self.httpKeytab.grid(row=20, column=0, sticky=W)       

        self.LabelCifsKeytab= Label(self, text="cifs Keytab Name: ")
        self.LabelCifsKeytab.grid(row = 21, column =0, sticky = W)
        self.cifsKeytab = Entry(self, width=100)
        self.cifsKeytab.grid(row=22, column=0, sticky=W)  

        self.LabelHTTPUserPass= Label(self, text="HTTP User Password: ")
        self.LabelHTTPUserPass.grid(row = 23, column =0, sticky = W)
        self.httpUserPass = Entry(self, width=100)
        self.httpUserPass.grid(row=24, column=0, sticky=W)

        self.alfHttpPasswordGen= Button(self, text="Create Password", command =self.acsHttpPasswordGen, state=DISABLED)
        self.alfHttpPasswordGen.grid(row=24, column=1, sticky=E)        
            
            
            
        self.checkBoxKrb5 = BooleanVar()
        self.krb5 = Checkbutton(self,text = "Create krb5.ini?",variable = self.checkBoxKrb5)
        self.krb5.grid(row = 30, column = 0, sticky = W)
            
                        
        self.checkBoxAD = BooleanVar()
        self.aD = Checkbutton(self, text = "Create service accounts, set SPNs, and Generate Keytabs for ACS?", variable = self.checkBoxAD,command = self.Active_Directory)
        self.aD.grid(row = 31, column = 0, sticky = W)
        
        
        
        
        
        #Create ACS AD Stuff Options  
        self.LabelHTTPUserDN= Label(self, text="HTTP User DistinguishedName: ", state=DISABLED)
        self.LabelHTTPUserDN.grid(row = 32, column =0, sticky = W)
        self.httpUserDN = Entry(self, state=DISABLED, width=100)
        self.httpUserDN.grid(row=33, column=0, sticky=W)
            
        self.LabelcifsUserDN= Label(self, text="cifs User DistinguishedName: ", state=DISABLED)
        self.LabelcifsUserDN.grid(row = 34, column =0, sticky = W)
        self.cifsUserDN = Entry(self, state=DISABLED, width=100)
        self.cifsUserDN.grid(row=35, column=0, sticky=W)      

        self.LabelCifsUserPass= Label(self, text="cifs User Password: ", state=DISABLED)
        self.LabelCifsUserPass.grid(row = 36, column =0, sticky = W)
        self.cifsUserPass = Entry(self, state=DISABLED, width=100)
        self.cifsUserPass.grid(row=37, column=0, sticky=W) 
        
        self.cifsPasswordGen= Button(self, text="Create Password", command =self.cifsPasswordGen, state=DISABLED)
        self.cifsPasswordGen.grid(row=37, column=1, sticky=E)
            
        self.LabelLdapAdminPS= Label(self, text="LDAP Administrator Domain\\Username: ", state=DISABLED)
        self.LabelLdapAdminPS.grid(row = 38, column =0, sticky = W)
        self.ldapAdminPS = Entry(self, state=DISABLED, width=100)
        self.ldapAdminPS.grid(row=39, column=0, sticky=W)      

        self.LabelLdapPassPS= Label(self, text="LDAP Administrator Password: ", state=DISABLED)
        self.LabelLdapPassPS.grid(row = 40, column =0, sticky = W)
        self.ldapPassPS = Entry(self, state=DISABLED, width=100)
        self.ldapPassPS.grid(row=41, column=0, sticky=W) 


        
        
        Label(self, text = "").grid(row = 80, column = 0, sticky = W)
        
        #Rollback ACS
        self.LabelRollACS= Label(self, text = "Rollback Alfresco (ACS) directory to original alfresco-global.properties and share-config-custom.xml?")
        self.LabelRollACS.grid(row = 81, column = 0, sticky = W)
        self.kerberosAR = Button(self, text = "Rollback ACS", command = self.Rollback_Original)
        self.kerberosAR.grid(row = 82, column = 0, sticky = W)

        
        
        
        
        
        
        
        
                
        #Alfresco Process Services Implement
        self.LabelAPS= Label(self, text = "Alfresco Process Services")
        self.LabelAPS.grid(row = 1, column = 0, sticky = W)
        
        self.toggleAPS = Button(self, text = "Toggle ACS", command = self.toggleAPS)
        self.toggleAPS.grid(row = 1, column = 0)        

        self.LabelDirAPS= Label(self, text="Activiti (APS) Install Directory: ")
        self.LabelDirAPS.grid(row = 51, column =0, sticky = W)
        self.dirAPS = Entry(self, width=100)
        self.dirAPS.grid(row=52, column=0, sticky=W)
            
        self.LabelServerNameAPS= Label(self, text="Activiti Server Name: ")
        self.LabelServerNameAPS.grid(row = 53, column =0, sticky = W)
        self.serverNameAPS = Entry(self, width=100)
        self.serverNameAPS.grid(row=54, column=0, sticky=W)
            
        self.LabelLdapFqdnAPS= Label(self, text="LDAP Fully Qualified Domain Name: ")
        self.LabelLdapFqdnAPS.grid(row = 55, column =0, sticky = W)
        self.ldapFqdnAPS = Entry(self, width=100)
        self.ldapFqdnAPS.grid(row=56, column=0, sticky=W)
            
        self.LabelAdminNameAPS= Label(self, text="LDAP Admin Name: ")
        self.LabelAdminNameAPS.grid(row =57, column =0, sticky = W)
        self.adminNameAPS = Entry(self, width=100)
        self.adminNameAPS.grid(row=58, column=0, sticky=W)
            
        self.LabelAdminPassAPS= Label(self, text="LDAP Admin Password: ")
        self.LabelAdminPassAPS.grid(row = 59, column =0, sticky = W)
        self.adminPassAPS = Entry(self, width=100)
        self.adminPassAPS.grid(row=60, column=0, sticky=W)
            
        self.LabelGroupBaseAPS= Label(self, text="LDAP Group Search Base: ")
        self.LabelGroupBaseAPS.grid(row = 61, column =0, sticky = W)
        self.groupBaseAPS = Entry(self, width=100)
        self.groupBaseAPS.grid(row=62, column=0, sticky=W)
            
        self.LabelUserBaseAPS= Label(self, text="LDAP User Search Base: ")
        self.LabelUserBaseAPS.grid(row = 63, column =0, sticky = W)
        self.userBaseAPS = Entry(self, width=100)
        self.userBaseAPS.grid(row=64, column=0, sticky=W)
            
        self.LabelKeytabPathAPS= Label(self, text="Keytab Path: ")
        self.LabelKeytabPathAPS.grid(row = 65, column =0, sticky = W)
        self.keytabPathAPS = Entry(self, width=100)
        self.keytabPathAPS.grid(row=66, column=0, sticky=W)
            
        self.LabelHTTPKeytabAPS= Label(self, text="HTTP Keytab Name: ")
        self.LabelHTTPKeytabAPS.grid(row = 67, column =0, sticky = W)
        self.httpKeytabAPS = Entry(self, width=100)
        self.httpKeytabAPS.grid(row=68, column=0, sticky=W)                     
            
            
            
        self.checkBoxKrb5APS = BooleanVar()
        self.krb5APS = Checkbutton(self,text = "Create krb5.ini?",variable = self.checkBoxKrb5APS)
        self.krb5APS.grid(row = 69, column = 0, sticky = W)
            
            
            
            
        self.checkBoxActivitiAD = BooleanVar()
        self.aDAPS = Checkbutton(self, text = "Create service accounts, set SPNs, and Generate Keytabs for APS?", variable = self.checkBoxActivitiAD,command = self.Active_Directory_Activiti)
        self.aDAPS.grid(row = 70, column = 0, sticky = W)
        
        
        
        
        
        # APS AD options        
        self.LabelHTTPUserDNAPS= Label(self, text="HTTP User DistinguishedName: ", state=DISABLED)
        self.LabelHTTPUserDNAPS.grid(row = 71, column =0, sticky = W)
        self.httpUserDNAPS = Entry(self, state=DISABLED, width=100)
        self.httpUserDNAPS.grid(row=72, column=0, sticky=W)
            
        self.LabelHTTPUserPassAPS= Label(self, text="HTTP User Password: ", state=DISABLED)
        self.LabelHTTPUserPassAPS.grid(row = 73, column =0, sticky = W)
        self.httpUserPassAPS = Entry(self, state=DISABLED, width=100)
        self.httpUserPassAPS.grid(row=74, column=0, sticky=W)
        
        self.actHttpPasswordGen= Button(self, text="Create Password", command =self.apsHttpPasswordGen, state=DISABLED)
        self.actHttpPasswordGen.grid(row=74, column=1, sticky=E)        
            
        self.LabelLdapAdminPSAPS= Label(self, text="LDAP Administrator Domain\\Username: ", state=DISABLED)
        self.LabelLdapAdminPSAPS.grid(row = 75, column =0, sticky = W)
        self.ldapAdminPSAPS = Entry(self, state=DISABLED, width=100)
        self.ldapAdminPSAPS.grid(row=76, column=0, sticky=W)      

        self.LabelLdapPassPSAPS= Label(self, text="LDAP Administrator Password: ", state=DISABLED)
        self.LabelLdapPassPSAPS.grid(row = 77, column =0, sticky = W)
        self.ldapPassPSAPS = Entry(self, state=DISABLED, width=100)
        self.ldapPassPSAPS.grid(row=78, column=0, sticky=W) 

        
        
        
        Label(self, text = "").grid(row = 80, column = 0, sticky = W)
        
        #Rollback Activiti
        self.LabelRollAPS= Label(self, text = "Rollback Activiti (APS) directory to original activiti-ldap.properties?                                                             ")
        self.LabelRollAPS.grid(row = 81, column = 0, sticky = W)
        self.kerberosAPSR = Button(self, text = "Rollback APS", command = self.Rollback_Original_Activiti)
        self.kerberosAPSR.grid(row = 82, column = 0, sticky = W)
        
        
        
        
        
        
        
        
        Label(self, text = "").grid(row = 99, column = 0, sticky = W)
        self.LabelMessage = Label(self, text = "")
        self.LabelMessage.grid(row = 100, column = 0, sticky = W)
        self.LabelMessage2 = Label(self, text = "")
        self.LabelMessage2.grid(row = 101, column = 0, sticky = W)
        Label(self, text = "").grid(row = 102, column = 0, sticky = W)
        
        
        
        #import config button
        self.importConfig = Button(self, text="Import Config", command=self.importConfig)
        self.importConfig.grid(row=1, column = 1, sticky=E)     
        
        
        
        
        #Run and Close Button
        self.runACS = Button(self, text="Run(ACS)", command=self.runACS)
        self.runACS.grid(row=110, column = 0, sticky=W)
        
        self.runAPS = Button(self, text="Run(APS)", command=self.runAPS)
        self.runAPS.grid(row=110, column = 0, sticky =W)
        
        
        
        self.close_button = Button(self, text="Close", command=self.quit)
        self.close_button.grid(row=110, column =1, sticky =E)
        
        
        
        
        
        
        
        
        
        #remove APS options by default
        self.LabelAPS.grid_remove()
        self.toggleAPS.grid_remove()
        self.LabelDirAPS.grid_remove()
        self.dirAPS.grid_remove()
        self.LabelServerNameAPS.grid_remove()
        self.serverNameAPS.grid_remove()
        self.LabelLdapFqdnAPS.grid_remove()
        self.ldapFqdnAPS.grid_remove()
        self.LabelAdminNameAPS.grid_remove()
        self.adminNameAPS.grid_remove()
        self.LabelAdminPassAPS.grid_remove()
        self.adminPassAPS.grid_remove()
        self.LabelGroupBaseAPS.grid_remove()
        self.groupBaseAPS.grid_remove()
        self.LabelUserBaseAPS.grid_remove()
        self.userBaseAPS.grid_remove()
        self.LabelKeytabPathAPS.grid_remove()
        self.keytabPathAPS.grid_remove()
        self.LabelHTTPKeytabAPS.grid_remove()
        self.httpKeytabAPS.grid_remove()

        
        #remove APS krb5 and AD options
        self.krb5APS.grid_remove()
        self.aDAPS.grid_remove()
        
        self.LabelHTTPUserDNAPS.grid_remove()
        self.httpUserDNAPS.grid_remove()
        self.LabelHTTPUserPassAPS.grid_remove()
        self.httpUserPassAPS.grid_remove()
        
        self.actHttpPasswordGen.grid_remove()
        
        self.LabelLdapAdminPSAPS.grid_remove()
        self.ldapAdminPSAPS.grid_remove()
        self.LabelLdapPassPSAPS.grid_remove()
        self.ldapPassPSAPS.grid_remove()
        
        self.LabelRollAPS.grid_remove()
        self.kerberosAPSR.grid_remove()
        self.runAPS.grid_remove()
        
        
        
        
        
        
        
        
        
    # Button for toggling ACS options       
    def toggleACS(self):
            
        
        
        
        #add APS options
        self.LabelAPS.grid()
        self.toggleAPS.grid()
        self.LabelDirAPS.grid()
        self.dirAPS.grid()
        self.LabelServerNameAPS.grid()
        self.serverNameAPS.grid()
        self.LabelLdapFqdnAPS.grid()
        self.ldapFqdnAPS.grid()
        self.LabelAdminNameAPS.grid()
        self.adminNameAPS.grid()
        self.LabelAdminPassAPS.grid()
        self.adminPassAPS.grid()
        self.LabelGroupBaseAPS.grid()
        self.groupBaseAPS.grid()
        self.LabelUserBaseAPS.grid()
        self.userBaseAPS.grid()
        self.LabelKeytabPathAPS.grid()
        self.keytabPathAPS.grid()
        self.LabelHTTPKeytabAPS.grid()
        self.httpKeytabAPS.grid()

        
        #add APS krb5 and AD options
        self.krb5APS.grid()
        self.aDAPS.grid()
        
        self.LabelHTTPUserDNAPS.grid()
        self.httpUserDNAPS.grid()
        self.LabelHTTPUserPassAPS.grid()
        self.httpUserPassAPS.grid()
        
        self.actHttpPasswordGen.grid()
        
        self.LabelLdapAdminPSAPS.grid()
        self.ldapAdminPSAPS.grid()
        self.LabelLdapPassPSAPS.grid()
        self.ldapPassPSAPS.grid()
        
        self.LabelRollAPS.grid()
        self.kerberosAPSR.grid()
        
        self.runAPS.grid()
        
        
        
        
        #remove ACS options
        self.LabelACS.grid_remove()
        self.toggleACS.grid_remove()
        self.LabelDir.grid_remove()
        self.dir.grid_remove()
        self.LabelServerName.grid_remove()
        self.serverName.grid_remove()
        self.LabelLdapFqdn.grid_remove()
        self.ldapFqdn.grid_remove()
        self.LabelAdminName.grid_remove()
        self.adminName.grid_remove()
        self.LabelAdminPass.grid_remove()
        self.adminPass.grid_remove()
        self.LabelGroupBase.grid_remove()
        self.groupBase.grid_remove()
        self.LabelUserBase.grid_remove()
        self.userBase.grid_remove()
        self.LabelKeytabPath.grid_remove()
        self.keytabPath.grid_remove()
        self.LabelHTTPKeytab.grid_remove()
        self.httpKeytab.grid_remove()
        self.LabelCifsKeytab.grid_remove()
        self.cifsKeytab.grid_remove()
        self.LabelHTTPUserPass.grid_remove()
        self.httpUserPass.grid_remove()
        
        #remove ACS krb5 and AD options
        self.krb5.grid_remove()
        self.aD.grid_remove()
        
        self.LabelHTTPUserDN.grid_remove()
        self.httpUserDN.grid_remove()
        self.LabelcifsUserDN.grid_remove()
        self.cifsUserDN.grid_remove()
        self.LabelCifsUserPass.grid_remove()
        self.cifsUserPass.grid_remove()
        
        self.cifsPasswordGen.grid_remove()
        self.alfHttpPasswordGen.grid_remove()
        
        self.LabelLdapAdminPS.grid_remove()
        self.ldapAdminPS.grid_remove()
        self.LabelLdapPassPS.grid_remove()
        self.ldapPassPS.grid_remove()
        
        self.LabelRollACS.grid_remove()
        self.kerberosAR.grid_remove()
        
        self.runACS.grid_remove()

        
        
        
        
        
        
        
        
        
    # Button for toggling ACS options       
    def toggleAPS(self):
        
        #add ACS options
        self.LabelACS.grid()
        self.toggleACS.grid()
        self.LabelDir.grid()
        self.dir.grid()
        self.LabelServerName.grid()
        self.serverName.grid()
        self.LabelLdapFqdn.grid()
        self.ldapFqdn.grid()
        self.LabelAdminName.grid()
        self.adminName.grid()
        self.LabelAdminPass.grid()
        self.adminPass.grid()
        self.LabelGroupBase.grid()
        self.groupBase.grid()
        self.LabelUserBase.grid()
        self.userBase.grid()
        self.LabelKeytabPath.grid()
        self.keytabPath.grid()
        self.LabelHTTPKeytab.grid()
        self.httpKeytab.grid()
        self.LabelCifsKeytab.grid()
        self.cifsKeytab.grid()
        self.LabelHTTPUserPass.grid()
        self.httpUserPass.grid()
        
        #add ACS krb5 and AD options
        self.krb5.grid()
        self.aD.grid()
        
        self.LabelHTTPUserDN.grid()
        self.httpUserDN.grid()
        self.LabelcifsUserDN.grid()
        self.cifsUserDN.grid()
        self.LabelCifsUserPass.grid()
        self.cifsUserPass.grid()
        
        self.cifsPasswordGen.grid()
        self.alfHttpPasswordGen.grid()
        
        self.LabelLdapAdminPS.grid()
        self.ldapAdminPS.grid()
        self.LabelLdapPassPS.grid()
        self.ldapPassPS.grid()
        
        self.LabelRollACS.grid()
        self.kerberosAR.grid()
        
        self.runACS.grid()
        
        
        
        
        
        #remove APS options
        self.LabelAPS.grid_remove()
        self.toggleAPS.grid_remove()
        self.LabelDirAPS.grid_remove()
        self.dirAPS.grid_remove()
        self.LabelServerNameAPS.grid_remove()
        self.serverNameAPS.grid_remove()
        self.LabelLdapFqdnAPS.grid_remove()
        self.ldapFqdnAPS.grid_remove()
        self.LabelAdminNameAPS.grid_remove()
        self.adminNameAPS.grid_remove()
        self.LabelAdminPassAPS.grid_remove()
        self.adminPassAPS.grid_remove()
        self.LabelGroupBaseAPS.grid_remove()
        self.groupBaseAPS.grid_remove()
        self.LabelUserBaseAPS.grid_remove()
        self.userBaseAPS.grid_remove()
        self.LabelKeytabPathAPS.grid_remove()
        self.keytabPathAPS.grid_remove()
        self.LabelHTTPKeytabAPS.grid_remove()
        self.httpKeytabAPS.grid_remove()

        
        #remove APS krb5 and AD options
        self.krb5APS.grid_remove()
        self.aDAPS.grid_remove()
        
        self.LabelHTTPUserDNAPS.grid_remove()
        self.httpUserDNAPS.grid_remove()
        self.LabelHTTPUserPassAPS.grid_remove()
        self.httpUserPassAPS.grid_remove()
        
        self.actHttpPasswordGen.grid_remove()
        
        self.LabelLdapAdminPSAPS.grid_remove()
        self.ldapAdminPSAPS.grid_remove()
        self.LabelLdapPassPSAPS.grid_remove()
        self.ldapPassPSAPS.grid_remove()
        
        self.LabelRollAPS.grid_remove()
        self.kerberosAPSR.grid_remove()
        
        self.runAPS.grid_remove()
            
            







        
    #this is for the active directory button wihtin the alfresco kerberos option.        
    def Active_Directory(self):
            
        # if its checked, enable additional fields    
        if self.checkBoxAD.get():
             
            self.LabelHTTPUserDN.configure(state="normal")
            self.httpUserDN.configure(state="normal")
                        
            self.LabelcifsUserDN.configure(state="normal")
            self.cifsUserDN.configure(state="normal")
   
            self.LabelCifsUserPass.configure(state="normal")
            self.cifsUserPass.configure(state="normal")
            
            self.cifsPasswordGen.configure(state="normal")
            self.alfHttpPasswordGen.configure(state="normal")
            
            self.LabelLdapAdminPS.configure(state="normal")
            self.ldapAdminPS.configure(state="normal")    

            self.LabelLdapPassPS.configure(state="normal")
            self.ldapPassPS.configure(state="normal")
            
            
        #if its unchecked, disable those additional options    
        else:
        
            self.LabelHTTPUserDN.configure(state="disabled")
            self.httpUserDN.configure(state="disabled")
                        
            self.LabelcifsUserDN.configure(state="disabled")
            self.cifsUserDN.configure(state="disabled")
   
            self.LabelCifsUserPass.configure(state="disabled")
            self.cifsUserPass.configure(state="disabled")
            
            self.cifsPasswordGen.configure(state="disabled")
            self.alfHttpPasswordGen.configure(state="disabled")
            
            self.LabelLdapAdminPS.configure(state="disabled")
            self.ldapAdminPS.configure(state="disabled")   

            self.LabelLdapPassPS.configure(state="disabled")
            self.ldapPassPS.configure(state="disabled")


            






            
   
    # this is for active directory options in the activiti kerberos configuration        
    def Active_Directory_Activiti(self):    
            
        # if checked, enable more options
        if self.checkBoxActivitiAD.get():
            
            self.LabelHTTPUserDNAPS.configure(state="normal")
            self.httpUserDNAPS.configure(state="normal")
            
            self.LabelHTTPUserPassAPS.configure(state="normal")
            self.httpUserPassAPS.configure(state="normal")
            
            self.actHttpPasswordGen.configure(state="normal")
            
            self.LabelLdapAdminPSAPS.configure(state="normal")
            self.ldapAdminPSAPS.configure(state="normal")      

            self.LabelLdapPassPSAPS.configure(state="normal")
            self.ldapPassPSAPS.configure(state="normal")
        
        
        #if unchecked, diable additional options
        else:
        
            self.LabelHTTPUserDNAPS.configure(state="disabled")
            self.httpUserDNAPS.configure(state="disabled")
            
            self.LabelHTTPUserPassAPS.configure(state="disabled")
            self.httpUserPassAPS.configure(state="disabled")
            
            self.actHttpPasswordGen.configure(state="disabled")
            
            self.LabelLdapAdminPSAPS.configure(state="disabled")
            self.ldapAdminPSAPS.configure(state="disabled")      

            self.LabelLdapPassPSAPS.configure(state="disabled")
            self.ldapPassPSAPS.configure(state="disabled")
            
            
            
           





           

        
        
        
                   
    #the function for when runACS button is clicked
    def runACS(self):

        #Declare initial checkbox values
        activeDirectoryI=False

        
        
    #############################################################################################
    #All below code is for when ACS is active#
    #############################################################################################
    
        #take the input and store it as variables
        #get set path
        pathI = self.dir.get()

        #get checkbox values of KRB5 and Active Directory
        krb5iniI= self.checkBoxKrb5.get()
        activeDirectoryI=self.checkBoxAD.get()
            


        #pull label values into variables
        alfServerI = self.serverName.get()
        ldapFQDN=self.ldapFqdn.get()
        ldapAdmin=self.adminName.get()
        ldapAdminPass=self.adminPass.get()
        ldapGroupBase=self.groupBase.get()
        ldapUserBase=self.userBase.get()
        keytabPath=self.keytabPath.get()
        httpKeytabName=self.httpKeytab.get()
        cifsKeytabName=self.cifsKeytab.get()
        httpPasswordI=self.httpUserPass.get()


        #strip domain from ldapFQDN
        start=ldapFQDN.find('.')+1
        domainI = ldapFQDN[start:]
        #domain I to uppercase for realm
        uDomainI = domainI.upper()
        #string text after period in domain for domainnetbios
        end=uDomainI.find('.')
        realm=uDomainI[0:end]



        #for if the kerberos alfresco active directory checkbox is checked, pull label values into variables
        #then make powershell calls to create accounts, set spns, and generate keytabs
        if (activeDirectoryI==True):

            httpUserDN=self.httpUserDN.get()
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
            
            
            
            
            
        #Keytab check definition call
        self.keytabChecker("ACS", pathI, keytabPath, httpKeytabName, alfServerI, cifsKeytabName)

            
            


            
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
            
            
            
                            
                
        #call to create krb5.ini
        if (krb5iniI==True):
            self.createKRB5("ACS")
            
            
            
        self.LabelMessage2.config(text="ACS configured for Kerberos")

            
    ####################################
    #End Alfresco Kerberos run function#
    ####################################

                
                
                
                
                
                
                
                
                        
    #the function for when runAPS button is clicked
    def runAPS(self):

    #############################################################################################
    #All below code is for when APS run is clicked#
    #############################################################################################
    
    
    
    
        #take the input and store it as variables
        #get set path
        pathI = self.dirAPS.get()
        

        #get APS checkbox values
        krb5iniI= self.checkBoxKrb5APS.get()
        activeDirectoryActivitiI=self.checkBoxActivitiAD.get()
            
            

            

        #pull label values into variables
        alfServerI = self.serverNameAPS.get()
        ldapFQDN=self.ldapFqdnAPS.get()
        ldapAdmin=self.adminNameAPS.get()
        ldapAdminPass=self.adminPassAPS.get()
        ldapGroupBase=self.groupBaseAPS.get()
        ldapUserBase=self.userBaseAPS.get()
        keytabPath=self.keytabPathAPS.get()
        httpKeytabName=self.httpKeytabAPS.get()


        #strip domain from ldapFQDN
        start=ldapFQDN.find('.')+1
        domainI = ldapFQDN[start:]
        #domain I to uppercase for realm
        uDomainI = domainI.upper()
        #string text after period in domain for domainnetbios
        end=uDomainI.find('.')
        realm=uDomainI[0:end]



        #for if the kerberos activiti active directory checkbox is checked, pull label values into variables
        if (activeDirectoryActivitiI==True):

            httpUserDN=self.httpUserDNAPS.get()
            httpPasswordI=self.httpUserPassAPS.get()
            psAdmin = self.ldapAdminPSAPS.get()
            psPass = self.ldapPassPSAPS.get()
            

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
            ps.write('\n\n')

            #write SPN setting commands to powershell file
            ps.write(r'#set the spns on the created service accounts')
            ps.write('\n')
            ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {setspn -a HTTP/'+alfServerI+'.'+domainI+' '+httpUserName+r'} -credential $cred')
            ps.write('\n')
            ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {setspn -a HTTP/'+alfServerI+' '+httpUserName+r'} -credential $cred')
            ps.write('\n\n')
                       
            #write delegation generating comamnds to powershell
            ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock {powershell "Set-ADAccountControl -Identity '+httpUserName+r' -TrustedForDelegation 1 -TrustedToAuthForDelegation 0"} -credential $cred')
            ps.write('\n\n')
            
            #write keytabs generation command to powershell file
            ps.write(r'#generate the keytabs and pull them back to the Alfresco server')
            ps.write('\n')
            ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock { md '+keytabPath+r'} -credential $cred')
            ps.write('\n\n')
            ps.write(r'Invoke-Command -ComputerName '+ldapFQDN+r' -ScriptBlock { ktpass -princ HTTP/'+alfServerI+r'@'+uDomainI+r' -pass '+httpPasswordI+' -mapuser '+realm+'\\'+httpUserName+r' -crypto RC4-HMAC-NT -ptype KRB5_NT_PRINCIPAL -out '+keytabPath+'\\'+httpKeytabName+r' -kvno 0} -credential $cred')
            ps.write('\n\n')
            ps.write(r'$SourceSession = New-PSSession -ComputerName '+ldapFQDN+r' -credential $cred')
            ps.write('\n\n')
            ps.write(r'Copy-Item -FromSession $SourceSession -Path "'+keytabPath+r'" -Destination "C:\" -Recurse')

            ps.close()
            
            # get the current working directory to find the powershell file
            cwd = os.getcwd()
            

            p = subprocess.Popen(["powershell.exe", cwd+r"\powershellAD.ps1"], stdout=sys.stdout)
            p.communicate()
            
            


            
        #Keytab check definition call
        self.keytabChecker("APS", pathI, keytabPath, httpKeytabName, alfServerI, "")
            


    
    
        #function to replace back slash ( \ ) with forward slash ( / ) in keytab path. Activiti Kerberos will not work with
        #backslashes in the kerberos.authenticaiton.keytab property when activiti is on windows        
        keytabPathSlash = keytabPath.replace("\\", "/")

        #copy the current activiti-ldap.properties file and re-write it with only needed lines          
        activitiLdapSource=pathI+r'\tomcat\lib\activiti-ldap.properties'
        activitiLdapOriginalCopy=pathI+r'\tomcat\lib\activiti-ldap.properties.original'

        shutil.copy(activitiLdapSource, activitiLdapOriginalCopy)



        with open(activitiLdapSource, 'w') as f0:

            f0.write('###Enable LDAP###')
            f0.write('\nldap.authentication.enabled=true')
            f0.write('\nldap.authentication.casesensitive=false')
            f0.write('\nldap.allow.database.authenticaion.fallback=true\n')
            
            f0.write('\n###Enable Synchronization###')
            f0.write('\nldap.synchronization.full.enabled=true')
            f0.write('\nldap.synchronization.full.cronExpression=0 0/3 * 1/1 * ?')
            f0.write('\nldap.synchronization.differential.enabled=false')
            f0.write('\nldap.synchronization.differential.cronExpression=0 0/2 * 1/1 * ?\n')
            
            f0.write('\n###Connection Settings###')                
            f0.write('\nldap.authentication.java.naming.provider.url=ldap://'+ldapFQDN+':389')
            f0.write('\nldap.synchronization.java.naming.security.principal='+ldapAdmin+'@'+domainI+'')
            f0.write('\nldap.synchronization.java.naming.security.credentials='+ldapAdminPass)                
            f0.write('\nldap.synchronization.java.naming.security.authentication=simple')
            f0.write('\nldap.authentication.java.naming.factory.initial=com.sun.jndi.ldap.LdapCtxFactory')
            f0.write('\nldap.synchronization.java.naming.referral=follow\n')
            
            f0.write('\n###User Sync Settings###')                
            f0.write('\nldap.synchronization.userSearchBase='+ldapUserBase)
            f0.write('\nldap.synchronization.personQuery=(objectClass\=user)')   
            f0.write('\nldap.synchronization.personDifferentialQuery=(&(objectclass\=user)(!(whenChanged<\={0})))')
            f0.write('\nldap.synchronization.userIdAttributeName=sAMAccountName')
            f0.write('\nldap.synchronization.userFirstNameAttributeName=givenName')
            f0.write('\nldap.synchronization.userLastNameAttributeName=sn')
            f0.write('\nldap.synchronization.userEmailAttributeName=mail')
            f0.write('\nldap.synchronization.userType=user\n')
            
            f0.write('\n###Group Sync Settings###')
            f0.write('\nldap.synchronization.groupSearchBase='+ldapGroupBase)
            f0.write('\nldap.synchronization.groupQuery=(objectClass\=group)')
            f0.write('\nldap.synchronization.groupDifferentialQuery=(&(objectclass\=group)(!(whenChanged<\={0})))')
            f0.write('\nldap.synchronization.groupIdAttributeName=cn')
            f0.write('\nldap.synchronization.groupMemberAttributeName=member')
            f0.write('\nldap.synchronization.groupType=group\n')
            
            f0.write('\n###Generic Attribut Settings###')
            f0.write('\nldap.synchronization.distinguishedNameAttributeName=dn')
            f0.write('\nldap.synchronization.modifyTimestampAttributeName=whenChanged')
            f0.write('\nldap.synchronization.createTimestampAttributeName=whenCreated')
            f0.write('\nldap.synchronization.timestampFormat=yyyyMMddHHmmss\'.0Z\'')
            f0.write('\nldap.synchronization.timestampFormat.locale.language=en')
            f0.write('\nldap.synchronization.timestampFormat.locale.country=US')
            f0.write('\nldap.synchronization.timestampFormat.timezone=GMT\n')
            
            f0.write('\n###Kerberos Settings###')
            f0.write('\nkerberos.authentication.enabled=true')
            f0.write('\nkerberos.authentication.principal=HTTP/'+alfServerI+'@'+uDomainI)
            f0.write('\nkerberos.authentication.keytab='+keytabPathSlash+'/'+httpKeytabName)
            f0.write('\n')
            f0.write(r'kerberos.authentication.krb5.conf=C:/Windows/krb5.ini')
            f0.write('\nkerberos.allow.ldap.authentication.fallback=true')
            f0.write('\nkerberos.allow.database.authentication.fallback=true')
            f0.write('\nkerberos.allow.samAccountName.authentication=true')
            f0.write('\nsecurity.authentication.use-externalid=true')
                
            f0.close()
        
            
            

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

            f3.write('\n\nAlfrescoHTTP {')
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
                
                
        
                
                
        #call to create krb5.ini
        if (krb5iniI==True):
            self.createKRB5("APS")
            
            
        self.LabelMessage2.config(text="APS configured for Kerberos")
            
    ####################################
    #End Activiti Kerberos run function#
    ####################################


            






            
    #Rollback Alfresco to original property files.
    def Rollback_Original(self):
    
        #get set path
        pathI = self.dir.get()
        
        #Rollback to the original configuration files in ACS
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
        
        
        
        
        self.LabelMessage.config(text="ACS rolled back to original property files.")
        
        
        
        
        
        
        
        
        
    # Rollback Activiti to Original files        
    def Rollback_Original_Activiti(self):
    
        #get set path
        pathI = self.dirAPS.get()


        activitiLdapCurrent=pathI+r'\tomcat\lib\activiti-ldap.properties'
        activitiLdapOriginalCopy=pathI+r'\tomcat\lib\activiti-ldap.properties.original'       
        shutil.copy(activitiLdapOriginalCopy, activitiLdapCurrent)
        os.remove(activitiLdapOriginalCopy)
        
        

        javaSecurityCurrent=pathI+r'\java\lib\security\java.security'
        javaSecurityOriginalCopy=pathI+r'\java\lib\security\java.security.original'
        shutil.copy(javaSecurityOriginalCopy, javaSecurityCurrent)
        os.remove(javaSecurityOriginalCopy)
        
        
        
        javaLoginConfigPath=pathI+r'\java\lib\security\java.login.config'
        os.remove(javaLoginConfigPath)
        
        
        
        self.LabelMessage.config(text="APS rolled back to original property files.")










    def createKRB5(self, product):
        
    #KRB5 is common between APS and ACS which is why it is at the end of the file in its own function
    
    #create krb5.ini
    
        if (product=="ACS"):
        
            ldapFQDN=self.ldapFqdn.get()
            
            
            
            
        if (product=="APS"):
        
            ldapFQDN=self.ldapFqdnAPS.get()


        #strip domain from ldapFQDN
        start=ldapFQDN.find('.')+1
        domainI = ldapFQDN[start:]
        #domain I to uppercase for realm
        uDomainI = domainI.upper()
        #string text after period in domain for domainnetbios
        end=uDomainI.find('.')
        realm=uDomainI[0:end]

        
            
    

        krb5iniPath=r'C:\Windows'
        krb5iniFile=r'krb5.ini'

        #simply create the file line by line adding the pulled varaibles from earlier.
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
            
            
            
            
            
            
            
            
            
            
    #ACS HTTP password generate
    def acsHttpPasswordGen(self):
    
        password = self.passwordGen()
        
        self.httpUserPass.delete(0, END)
        self.httpUserPass.insert(0, password)

        
        
        

    #ACS CIFS password generate
    def cifsPasswordGen(self):
    
        password = self.passwordGen()
        
        self.cifsUserPass.delete(0, END)
        self.cifsUserPass.insert(0, password)
        
        
        
        
        
    #APS HTTP password generate    
    def apsHttpPasswordGen(self):
    
        password = self.passwordGen()
        
        self.httpUserPassAPS.delete(0, END)
        self.httpUserPassAPS.insert(0, password)
        
    
    
    
    
    # used for generating passwords to use when creating service accounts       
    def passwordGen(self):
    
        capChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lowChars = 'abcdefghijklmnopqrstuvwxyz'
        numChars = '0123456789'
        speChars= r'!@#$%^&*()-_=+[{]}|\\:;"\',<.>?/~'
        allChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[{]}|\\:;"\',<.>?/~'
        
        password=''
        
        #to ensure that each password has Upper, Lower, Number, and Special characters
        password = random.choice(capChars) + random.choice(lowChars) + random.choice(numChars) + random.choice(speChars)
        
        i = random.randint(6,16)
        
        for c in range(i):
            password = password + random.choice(allChars)
            
        return password
        
        
        
        
    
    #definition to run when Import Config button is used. Read from kerberosConfig.config file in same directory
    def importConfig(self):
        
        # get the current working directory to find the config file
        cwd = os.getcwd()
        
        configFile=r'kerberosConfig.config'

        #read the config file.
        with open(os.path.join(cwd, configFile), 'r') as config:
        
            #Iterate through entire config file, when there is a matching entry, read the next line as the property and save to UI
            for line in config:
                
                #ACS options
                if ('Alfreco (ACS) Install Directory:' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.dir.delete(0, END)
                    self.dir.insert(0, rLine)
                    
                    
                elif ('Alfresco Server Name:' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.serverName.delete(0, END)
                    self.serverName.insert(0, rLine)
                    

                elif ('LDAP Fully Qualified Domain Name(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.ldapFqdn.delete(0, END)
                    self.ldapFqdn.insert(0, rLine)

                elif ('LDAP Admin Name(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.adminName.delete(0, END)
                    self.adminName.insert(0, rLine)

                elif ('LDAP Admin Password(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.adminPass.delete(0, END)
                    self.adminPass.insert(0, rLine)
                    
                elif ('LDAP Group Search Base(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.groupBase.delete(0, END)
                    self.groupBase.insert(0, rLine)
                    
                elif ('LDAP User Search Base(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.userBase.delete(0, END)
                    self.userBase.insert(0, rLine)
                    
                elif ('Keytab Path(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.keytabPath.delete(0, END)
                    self.keytabPath.insert(0, rLine)
                    
                elif ('HTTP Keytab Name(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.httpKeytab.delete(0, END)
                    self.httpKeytab.insert(0, rLine)
                    
                elif ('cifs Keytab Name:' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.cifsKeytab.delete(0, END)
                    self.cifsKeytab.insert(0, rLine)
                    
                elif ('HTTP User Password(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.httpUserPass.delete(0, END)
                    self.httpUserPass.insert(0, rLine)
                    
                elif ('Create krb5.ini(ACS)?' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    if (rLine =='y' or rLine=='yes'):
                        self.krb5.select()
                    
                elif ('Create service accounts, set SPNs, and Generate Keytabs for ACS?' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    if (rLine =='y' or rLine=='yes'):
                        self.aD.select()
                        self.Active_Directory()
                        
                elif ('HTTP User DistinguishedName(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.httpUserDN.delete(0, END)
                    self.httpUserDN.insert(0, rLine)
                    
                elif ('cifs User DistinguishedName:' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.cifsUserDN.delete(0, END)
                    self.cifsUserDN.insert(0, rLine)
                    
                elif ('cifs User Password:' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.cifsUserPass.delete(0, END)
                    self.cifsUserPass.insert(0, rLine)
                    
                elif (r'LDAP Administrator Domain\Username(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.ldapAdminPS.delete(0, END)
                    self.ldapAdminPS.insert(0, rLine)
                    
                elif ('LDAP Administrator Password(ACS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.ldapPassPS.delete(0, END)
                    self.ldapPassPS.insert(0, rLine)
                    
                    
                    
                    
                    
                #APS options
                elif ('Activiti (APS) Install Directory:' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.dirAPS.delete(0, END)
                    self.dirAPS.insert(0, rLine)
                    
                    
                elif ('Activiti Server Name:' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.serverNameAPS.delete(0, END)
                    self.serverNameAPS.insert(0, rLine)
                    

                elif ('LDAP Fully Qualified Domain Name(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.ldapFqdnAPS.delete(0, END)
                    self.ldapFqdnAPS.insert(0, rLine)

                elif ('LDAP Admin Name(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.adminNameAPS.delete(0, END)
                    self.adminNameAPS.insert(0, rLine)

                elif ('LDAP Admin Password(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.adminPassAPS.delete(0, END)
                    self.adminPassAPS.insert(0, rLine)
                    
                elif ('LDAP Group Search Base(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.groupBaseAPS.delete(0, END)
                    self.groupBaseAPS.insert(0, rLine)
                    
                elif ('LDAP User Search Base(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.userBaseAPS.delete(0, END)
                    self.userBaseAPS.insert(0, rLine)
                    
                elif ('Keytab Path(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.keytabPathAPS.delete(0, END)
                    self.keytabPathAPS.insert(0, rLine)
                    
                elif ('HTTP Keytab Name(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.httpKeytabAPS.delete(0, END)
                    self.httpKeytabAPS.insert(0, rLine)
                    
                elif ('HTTP User Password(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.httpUserPassAPS.delete(0, END)
                    self.httpUserPassAPS.insert(0, rLine)
                    
                elif ('Create krb5.ini(APS)?' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    if (rLine =='y' or rLine=='yes'):
                        self.krb5APS.select()
                    
                elif ('Create service accounts, set SPNs, and Generate Keytabs for APS?' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    if (rLine =='y' or rLine=='yes'):
                        self.aDAPS.select()
                        self.Active_Directory_Activiti()
                        
                elif ('HTTP User DistinguishedName(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.httpUserDNAPS.delete(0, END)
                    self.httpUserDNAPS.insert(0, rLine)
                    
                elif (r'LDAP Administrator Domain\Username(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.ldapAdminPSAPS.delete(0, END)
                    self.ldapAdminPSAPS.insert(0, rLine)
                    
                elif ('LDAP Administrator Password(APS):' in line):
                    rLine = config.readline()
                    rLine = rLine.replace("\n", "").replace(" ", "")
                    
                    self.ldapPassPSAPS.delete(0, END)
                    self.ldapPassPSAPS.insert(0, rLine)
                    
                    
                    
                    
                    
                    
                    
                    
    
    #automated keytab checker
    def keytabChecker(self, product, pathI, keytabPath, httpKeytabName, alfServerI, cifsKeytabName):
        
        if (product =='ACS'):

            command=pathI+r'\java\bin\kinit.exe -k -t "'+keytabPath+'\\'+httpKeytabName+r'" "HTTP/'+alfServerI+r'"'
            #print (command)
            
            p = subprocess.Popen(command, stdout=sys.stdout)
            p.communicate()
            
            
            command=pathI+r'\java\bin\kinit.exe -k -t "'+keytabPath+'\\'+cifsKeytabName+r'" "cifs/'+alfServerI+r'"'
            #print (command)
            
            p = subprocess.Popen(command, stdout=sys.stdout)
            p.communicate()
            
        elif (product=='APS'):
        
            command=pathI+r'\java\bin\kinit.exe -k -t "'+keytabPath+'\\'+httpKeytabName+r'" "HTTP/'+alfServerI+r'"'
            #print (command)
            
            p = subprocess.Popen(command, stdout=sys.stdout)
            p.communicate()
                    
            

            

        
        
            
      

root = Tk()
root.title("Kerberos Configurer")
app = Application(root)
root.mainloop()