# setting up the parameter hashes
ldapProperties = ['realmName','ldapHost','ldapPort','ldapServerType','baseDN','bindDN','bindPassword','searchTimeout','sslConfig','reuseConnection','ignoreCase','sslEnabled','verifyRegistry','userFilter','groupFilter','userIdMap','groupMemberIdMap','certificateFilter','certificateMapMode','customProperties','verifyRegistry']

csiInboundSettings = ["messageLevelAuth","supportedAuthMechList","clientCertAuth","transportLayer","sslConfiguration","enableIdentityAssertion","statefulSession","enableAttributePropagation","trustedIdentities"]

csiOutboundSettings = ["messageLevelAuth","supportedAuthMechList","clientCertAuth","transportLayer","sslConfiguration","enableIdentityAssertion","statefulSession","enableAttributePropagation","trustedId","useServerIdentity","trustedIdentityPassword","trustedTargetRealms","enableCacheLimit","maxCacheSize","idleSessionTimeout"]

# check if the securityDomain exists .. if it does .. start fresh
if securityDomainExists(deployed.name):	
  destroySecurityDomain(deployed.name)	

# create the securityDomain
AdminTask.createSecurityDomain(['-securityDomainName', deployed.name, '-securityDomainDescription', deployed.description])
print "security domain: %s created" % deployed.name

#map the security domain
for ci in deployed.mapping:
   removeResourcesFromSecurityDomain(deployed.name)
   if not resourceExistsInSecurityDomain(ci.name, deployed.name):
     AdminTask.mapResourceToSecurityDomain("-securityDomainName %s -resourceName Cell=:ServerCluster=%s" % (deployed.name, ci.name))
     print "succesfully mapped securityDomain %s to %s" % (deployed.name, ci.name)

# check if we need to setup Ldap
if deployed.SetupLdap:
 #Full Ldap setup
 #adminTaskProperties="-securityDomainName %s %s" % (deployed.name, formatAdminTaskParameters(ldapProperties,"ldaP"))
 runAdminTaskCommand('configureAppLDAPUserRegistry', "-securityDomainName %s %s" % (deployed.name, formatAdminTaskParameters(ldapProperties,"ldaP")))
 #advanced search filters and stuff 


#setup LTPA TimeOut
print "setting up the ltpa timeout" 
AdminTask.setLTPATimeout("-securityDomainName %s -timeout %i " % (deployed.name, deployed.ltpaTimeout))
print "LTPA timeout setting set to %i" % deployed.ltpaTimeout 

#CSIInbound config
if deployed.SetupCsiInbound:
 #Full Ldap setup
 runAdminTaskCommand('configureCSIInbound', "-securityDomainName %s %s" % (deployed.name, formatAdminTaskParameters(csiInboundSettings,"csiI")))
 #advanced search filters and stuff

#CSIOutbound config
if deployed.SetupCsiInbound:
 #Full Ldap setup
 runAdminTaskCommand('configureCSIOutbound', "-securityDomainName %s %s" % (deployed.name, formatAdminTaskParameters(csiInboundSettings,"csiO")))
 #advanced search filters and stuff
