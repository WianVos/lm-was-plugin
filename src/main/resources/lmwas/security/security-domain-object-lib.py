def securityDomainExists(scName):
        for domain in AdminTask.listSecurityDomains('[-listDescription false]').splitlines():
          if domain == scName:
            print "security domain: %s exists .. no worries m8" % scName
            return True
        else:
          print "security domain: %s exists... ha a small panic attack... now" % scName

def resourceExistsInSecurityDomain(resource, scName):
  for resourceId in wsadminToList(AdminTask.listResourcesInSecurityDomain("-securityDomainName %s" % (scName))):
        if resourceId.find(resource) >= 0:
          print "resource %s is mapped to SecurityDomain %s" % (resource, scName)
          return True

  print "resource %s is not mapped to SecurityDomain %s" % (resource, scName)
  return False

def removeResourcesFromSecurityDomain(scName):
  try:
   for resourceId in wsadminToList(AdminTask.listResourcesInSecurityDomain("-securityDomainName %s -expandCell true" % (scName))):
    resourceId = resourceId.replace("Cluster=", "ServerCluster=")
    print resourceId
    AdminTask.removeResourceFromSecurityDomain("-securityDomainName %s -resourceName %s" % (scName, resourceId))
    print "resource: %s was removed from security domain %s" % (resourceId, scName)
  except:
    print "attempt to remove all resources from securitydomain: %s failed" % (scName)
    raise

def destroySecurityDomain(scName):
 if securityDomainExists(scName):
  removeResourcesFromSecurityDomain(scName)
  AdminTask.deleteSecurityDomain(['-securityDomainName', scName])
  print "security domain: %s destroyed" % scName

def formatAdminTaskParameters(options, prefix):
 adminTaskProperties = ""
 for option in options:
   adminTaskProperty = ""
   print option
    
  
   if hasattr(deployed, "%s%s" % (prefix, option)):
    print "prefixed: %s option %s found" % (prefix, option)
    deployedOption = "%s%s" % (prefix, option)
   elif hasattr(deployed, "%s" % (option)): 
    print "found unprefixed option: %s , running with that"  
    deployedOption = option
   else:
    deployedOption = ""
   
   if hasattr(deployed, deployedOption):

    if str(getattr(deployed, deployedOption)) != "":
     print str(getattr(deployed, deployedOption))
     optionType = type(getattr(deployed, deployedOption))

     if str(optionType) == "org.python.core.PyDictionary":
	
        print "bla"
        print adminTaskProperty

        adminTaskProperty = ""
        customPropertiesString="["
	for key, value in tuple(getattr(deployed, deployedOption).items()):
	   customPropertiesString+= '"%s=%s",' % (key, value)
        if customPropertiesString != "[":
         adminTaskProperty = customPropertiesString + "]"
         adminTaskProperty = adminTaskProperty.replace(',]',']')
         if adminTaskProperty == "[]":
          adminTaskProperty = "" 
         print option
         adminTaskProperty = ' -%s %s' % (option, adminTaskProperty)
        
     if str(optionType) == 'org.python.core.PyString':
       adminTaskProperty = " -%s %s" % (option, getattr(deployed, deployedOption))

     if str(optionType) == 'org.python.core.PyInteger':
       if hasattr(deployed, "%s_as_string" %(deployedOption)):
         adminTaskProperty = " -%s %s" % (option, getattr(deployed, "%s_as_string" % (deployedOption)))
       else:
         adminTaskProperty = " -%s %s" % (option, getattr(deployed, deployedOption))

     adminTaskProperties += adminTaskProperty

 return adminTaskProperties

def runAdminTaskCommand(subcommand, parameters):
  command = "AdminTask.%s('%s')" % (subcommand, parameters)
  print "running %s" % command
  exec command  
