# Kerberos Configurer

Placeholder document for Kerberos Configurer manual.

## Sample Input Format:

Implement Kerberos Configurations in the Alfresco (ACS) Directory? 

Alfresco (ACS) Install Directory:
C:\Alfresco521Directory

AlfrescoServerName: 
AlfrescoServerName1

LDAP Fully Qualified Domain Name: 
KerberosDomainController.domain.com

LDAP Admin Name: 
Administrator

LDAP Admin Password: 
Alfr3sc0!

LDAP Group Search Base: 
OU=KerberosGroups,DC=domain,DC=com

LDAP User Search Base: 
OU=KerberosUsers,DC=domain,DC=com

Keytab Path: 
C:\alfKerbKeys

HTTP Keytab Name:
KerbHTTP.keytab

cifs Keytab Name
Kerbcifs.keytab

HTTP User Password:
servic3AccountP@ssword




Create Service Accounts, set SPNs, and Generate Keytabs for ACS?

HTTP User DistinguishedName: 
cn=HTTPServiceAccount,cn=users,dc=domain,dc=com

cifs User DistinguishedName:
cn=cifsServiceAccount,cn=users,dc=domain,dc=com

cifs User Password: 
servic3AccountP@ssword

Enter LDAP Administrator Domain\Username: 
domain.com\Administrator

Enter LDAP Administrator Password:
LdapAdminP@ssw0rd