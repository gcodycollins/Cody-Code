##############################################
#
# Created by Grayson Cody Collins
#
# Please reach out to cody.collins@alfresco.com or skypeId cody.collins_3
# with any questions, improvements, or requests.
#
##############################################

##############################################
#
# Used to create a .csv file for import of NTLM users directly to Alfresco 
#
##############################################

#accept input
fileName= input("Name of csv file (minus '.csv'): ")
uCount= input("Number of users to create: ")
fName= input("Users first name (an incrementer will be appended): ")
lName= input("Users last name (an incrementer will be appended): ")
uPassword= input("Password to set for users: ")

#blank out file first before writing.
f = open(fileName+'.csv','w').close()
#open file to write output to
f = open(fileName+'.csv','w')

f.write('User Name,First Name,Last Name,E-mail Address,Pasword,Company,Job Title,Location,Telephone,Mobile,Skype,IM,Google User Name,Address,Address Line 2,Address Line 3,Post Code,Telephone,Fax,Email\n')

for i in range (0,int(uCount)):
    f.write(fName+str(i)+'.'+lName+str(i)+','+fName+str(i)+','+lName+str(i)+','+lName+str(i)+'@test.m'+','+uPassword+',,,,,,,,,,,,,,,\n')
f.close()