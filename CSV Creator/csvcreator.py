#accept input
fileName= input("Name of csv file (minus '.csv'): ")
uCount= input("Number of users to create: ")
domain= input("Domain: ")
ou= input("OU to create users in (EX: OU=testUsers,DC=Stealth,DC=Ace): ")
fName= input("Users first name (an incrementer will be appended): ")
lName= input("Users last name (an incrementer will be appended): ")
uPassword= input("Password to set for users: ")

#blank out file first before writing.
f = open(fileName+'.csv','w').close()
#open file to write output to
f = open(fileName+'.csv','w')

f.write('"Domain","Path","FirstName","LastName","Office","Title","Description","Department","Company","Phone","StreetAddress","City","State","PostalCode","Password","sAMAccountName","userPrincipalName","DisplayName"\n')

for i in range (0,int(uCount)):
    f.write(domain+' , "'+ou+'" , '+fName+str(i)+' , '+lName+str(i)+' ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  , \"'+uPassword+'\" , '+fName+str(i)+lName+str(i)+' ,  \"'+fName+str(i)+lName+str(i)+'@'+domain+'\" ,'+fName+str(i)+lName+str(i)+'\n')
f.close()