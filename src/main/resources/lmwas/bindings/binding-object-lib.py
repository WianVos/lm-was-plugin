def setSCAImportWSBinding (attributes):
  print " Setting " + attributes['serviceName'] + "  to " + attributes['bindURL'] + " for " + attributes['moduleName']
  AdminTask.modifySCAImportWSBinding("-moduleName %s -applicationName %s -import %s -endpoint %s" % (attributes['moduleName'], attributes['applicationName'], attributes['serviceName'], attributes['bindURL']))

#------

def setGeneralClientPolicySet (attributes):
  output = AdminTask.getPolicySetAttachments('[-applicationName %s -attachmentType client]' % (attributes['applicationName'])).replace(' ','=').replace(']=[',';').replace('[=[','').replace(']=]','')
  print output
  adDict = {}
  for x in output.split(';'):
   key, value = x.split('=')
   adDict[key] = value


  try:
    print AdminTask.setBinding("-bindingScope domain -bindingName %s -attachmentType %s -bindingLocation [ [application %s] [attachmentId %s] ]" % (attributes['bindingName'], attributes['attachmentType'], attributes['applicationName'], adDict['id']))
    print "attached %s to application: %s" % (attributes['bindingName'], attributes['applicationName'])
  except:
    print "unable to attach %s to application: %s" % (attributes['bindingName'], attributes['applicationName'])
    raise

#------

def setApplicationClientPolicySet (attributes):
  print " Setting " + attributes['attachmentType'] + "  PolicySet for webservice " + attributes['serviceName'] + " to: " + attributes['policySet']
  AdminTask.createPolicySetAttachment("-applicationName %s -attachmentType %s -policySet %s -resources [WebService:/%s:{%s}%s ]" % (attributes['applicationName'], attributes['attachmentType'], attributes['policySet'], attributes['webModuleName'], attributes['namespace'], attributes['serviceName']))
 
#------

def setWebModContextRoot(attributes):
  print " Setting Context root" + attributes['contextRoot'] + " for Module:  " + attributes['applicationName']
  AdminApp.edit(attributes['applicationName'], ["-CtxRootForWebMod", [[attributes['webModuleName'], attributes['uri'], attributes['contextRoot']]]])

#------
#This doesnt work syntax error, also need to review wsadmintoList function.
def setActivationSpecMaxConcurrency (attributes):
  newMaxConn = str(attributes['maxConcurrency'])
  if newMaxConn.isdigit():
    ActSpecs = AdminConfig.list('J2CActivationSpec').splitlines()
    for ActSpec in ActSpecs:
      if ActSpec.find(attributes['activationSpecName']) != -1:
        ActSpecAtt = AdminConfig.showAttribute(ActSpec, 'resourceProperties')
        ActSpecAttList = wsadminToList(ActSpecAtt)
        for i in ActSpecAttList:
          if i.find('maxConcurrency') != -1:
            try:
              AdminConfig.modify(i, [['value', newMaxConn]])
            except:
              print "Unable to locate max concurrency setting for the specified Activation Spec"
              raise
  else:
    print "The max concurrency specified: %s is not an integer, please provide a proper value." % (attributes['maxConcurrency'])
    raise

#------

def setModuleProperty(attributes):
  print "Setting %s to %s for %s" % (attributes['propertyName'], attributes['propertyValue'], attributes['moduleName'])
  AdminTask.modifySCAModuleProperty(['-moduleName', attributes['moduleName'], '-propertyName', attributes['propertyName'], '-newPropertyValue', attributes['propertyValue']])

#------

def setJNDIforEJBnonMDB(attributes):
  print "Setting EJB attributes for %s" % (attributes['appName'])
  AdminApp.edit(attributes['appName'], ["-BindJndiForEJBNonMessageBinding", [[attributes['ejbModule'], attributes['ejbName'], attributes['moduleUri'], attributes['newJndi']]]])

#------

def setSCAImportHttpBindingSSLConfiguration(attributes):
  print "Assigning SSL settings to %s in %s" % (attributes['importName'], attributes['moduleName'])
  tagName = stringExistCheck(attributes['importName'], attributes['methodName']) 
  AdminTask.modifySCAImportHttpBinding("-moduleName %s -import %s -endpointURL <%s>%s</%s> -sslConfiguration <%s>%s</%s>" % (attributes['moduleName'], attributes['importName'], tagName, attributes['newUrl'], tagName, tagName, attributes['sslConfiguration'], tagName))

#------

def setSCAImportHttpBindingWithAuth(attributes):
  print "Assigning auth settings to %s in %s" % (attributes['importName'], attributes['moduleName'])
  tagName = stringExistCheck(attributes['importName'], attributes['methodName'])
  AdminTask.modifySCAImportHttpBinding("-moduleName %s -import %s -endpointURL <%s>%s</%s>  -authAlias <%s>%s</%s>" % ( attributes['moduleName'],  attributes['importName'], tagName,  attributes['newUrl'], tagName, tagName,  attributes['j2cAuthName'], tagName))

#------

def setSCAImportHttpBinding(attributes):
  print "Setting %s in %s to %s with a timeout value of %s" % (attributes['importName'], attributes['moduleName'], attributes['newUrl'], attributes['newTimeout'])
  tagName = stringExistCheck(attributes['importName'], attributes['methodName'])
  AdminTask.modifySCAImportHttpBinding("-moduleName %s -import %s -endpointURL <%s>%s</%s> -responseReadTimeout <%s>%s</%s>" % (attributes['moduleName'], attributes['importName'], tagName, attributes['newUrl'], tagName, tagName, attributes['newTimeout'], tagName))

#------

def setSCAImportBindingProxy(attributes):
  tagName = stringExistCheck(attributes['importName'], attributes['methodName'])
  protocol = attributes['protocolType'] 
  protocol = protocol.lower()
  if protocol == 'http':
    print "Setting %s proxy in %s. Setting Proxy Host to %s, and Proxy Port to %s" % (protocol, attributes['moduleName'], attributes['newProxyHost'], attributes['newProxyPort'])
    AdminTask.modifySCAImportHttpBinding("-moduleName %s -import %s -httpProxyHost <%s>%s</%s> -httpProxyPort <%s>%s</%s>" % (attributes['moduleName'], attributes['importName'], tagName, attributes['newProxyHost'], tagName, tagName, attributes['newProxyPort'], tagName))
  elif protocol == 'https':
    print "Setting %s proxy in %s. Setting Proxy Host to %s, and Proxy Port to %s" % (protocol, attributes['moduleName'], attributes['newProxyHost'], attributes['newProxyPort'])
    AdminTask.modifySCAImportHttpBinding("-moduleName %s -import %s -httpsProxyHost <%s>%s</%s> -httpsProxyPort <%s>%s</%s>" % (attributes['moduleName'], attributes['importName'], tagName, attributes['newProxyHost'], tagName, tagName, attributes['newProxyPort'], tagName))
  else:
    raise ValueError('Please use a valid Protocol Type.  Valid types include http or https')

#------

def setSCAImportHttpBindingConnectionRetries(attributes):
  print "Setting Retry Value to %s for %s in %s" % (attributes['newRetriesValue'], attributes['importName'], attributes['importName'])
  tagName = stringExistCheck(attributes['importName'], attributes['methodName'])
  AdminTask.modifySCAImportHttpBinding("-moduleName %s -import %s -connectionRetries <%s>%s</%s>" % (attributes['moduleName'], attributes['importName'], tagName, attributes['newRetriesValue'], tagName))

#------

def setWSClientBindings(attributes):
  print " Setting service: %s with client bindings for %s" % (attributes['webServiceName'], attributes['applicationName'])
  AdminApp.edit(attributes['applicationName'], ["-WebServicesClientBindPortInfo", [[attributes['ejbModuleName'], attributes['ejbName'], attributes['webServiceName'], attributes['portName'], xstr(attributes['timeoutValue']), xstr(attributes['authId']), xstr(attributes['authPassword']), "", xstr(attributes['bindUrl'])]]])

#------

def setDestinationMaxRetries(attributes):
    #confirm a valid Bus is being requested
    suppliedBusName = attributes['busName']
    legalShortNames = ['SCA.SYSTEM', 'SYSTEM', 'SCA.APPLICATION', 'APPLICATION']
    fullBusName = ''

    #list of Buses in this Cell
    SIBusList = AdminTask.listSIBuses().split("\n")
    SIBusNameList = []
    for Bus in SIBusList:
        BusFullQual = Bus.rstrip()
        siBusName = AdminConfig.showAttribute(BusFullQual, "name")
        SIBusNameList.append(siBusName)

    #now check if the busName is already in the list
    if suppliedBusName in SIBusNameList:
        fullBusName = suppliedBusName

    else:
        #see if the busName is an acceptable shortname version
        if suppliedBusName in legalShortNames:
            #now determine the fully qualified SIBusName
            for bus in SIBusNameList:
                print bus.find(suppliedBusName)
                if bus.find(suppliedBusName) > -1:
                    fullBusName = bus
        else:
            print "Bus %s does not appear to match a bus in this Cell" % (suppliedBusName)
            raise ValueError('Please ensure the bus specified exists in this Cell')
    newValue = str(attributes['failedDeliveryCount'])
    if newValue.isdigit():
        print "Setting Max Failed Deliveries to %s for %s" % (newValue, attributes['destinationName'])
        AdminTask.modifySIBDestination(["-bus", fullBusName, "-name", attributes['destinationName'], "-maxFailedDeliveries", newValue])

#------

def setMDBRetries(attributes):
  newValue = str(retryCount)
  lPort = adm.getID('/ListenerPort:"%s("' % (attributes['mdbName']))
  print "Setting Max Retries to %s for %s" % (newValue, attributes['mdbName'])
  AdminConfig.modify(lPort, [["maxRetries", newValue]])

#------

def setSharedLibraryForModule(attributes):
  print "Setting shared libraries for %s" % (attributes['applicationName'])
  AdminApp.edit(attributes['applicationName'], ['-MapSharedLibForMod', [[attributes['applicationName'], 'META-INF/application.xml', attributes['sharedLibrariesName']]]])

#------

def wsadminToList(inStr):
    """
    Take a default string format from a wsadmin command and generate a Python list

    Arguments:
    inString - (string)

    Returns:
    a list
    """

    outList=[]
    if (len(inStr)>0 and inStr[0]=='[' and inStr[-1]==']'):
        tmpList = inStr[1:-1].split(" ")
    else:
        tmpList = inStr.split("\n") #splits for Windows or Linux
    for item in tmpList:
        item = item.rstrip(); #removes any Windows "\r"
        if (len(item)>0):
            outList.append(item)
    return outList

#------

def stringExistCheck (importName, methodName):
  
  stringCheck = xstr(methodName)
  if not stringCheck:
    tagName = importName
    print "Method was blank, using import"
  else:
    tagName = methodName
    print "Method was set"
  return tagName

#------

def policyAttachmentExists(policySet, application):
  attachments = AdminTask.listAttachmentsForPolicySet(['-policySet', policySet ]).splitlines()

  for a in attachments:
   if application == a :
     print "policy set %s is attached to %s" % (policySet, application)
     return True
   print "policy set %s is NOT attached to %s" % (policySet, application)
   return False

#------

def policySetExists (name, policySetType):
  policysets = AdminTask.listPolicySets(['-policySetType', policySetType]).splitlines()

  for s in policysets:
   if name == s :
    print "policy set %s exists" % (name)
    return True

  print "policy set %s does not exists" % (name)
  return False

#------

def bindingAsHash(binding):
  unwantedProperties = ['container','deployable', 'name', 'id', 'bindingType', 'bindingOrder', 'type']
  returnHash = {}
  for property in binding._properties:
    if property not in unwantedProperties:
      if isinstance(getattr(binding, property), DictionaryObject):
        if property == "customProperties":
          returnHash[property] = getattr(binding, property)
        else:
          returnHash[str(getattr(binding,property).name)] = str(getattr(binding,property).value)
      else:
        returnHash[property] = getattr(binding, property)

  return returnHash

#------

def toEnclosedAttrString(attributes, startChar, endChar):
    print attributes
    argString = ""
    for attrName, attrValue in attributes.items():
        if attrName == "customProperties":
          argString += customPropertiesToEnclosedAttrString(attrValue)
        elif attrValue != None:
            if isinstance(attrValue, DictionaryObject):
                argString += "%s'%s' '%s'%s" % (startChar, attrName, str(attrValue.name), endChar)
            else:
                argString += "%s'%s' '%s'%s" % (startChar, attrName, str(attrValue), endChar)
    return "%s%s%s" % (startChar, argString, endChar)

#-----

#Replace None with blank value
def xstr(s):
    if s is None:
        return ''
    return str(s)

#-----

def customPropertiesToEnclosedAttrString(attributes):
  argString = ""
  counter = 0
  for attrName, attrValue in attributes.items():
    argString += "%s'%s' '%s'%s" % ('[', "properties_%i:name" % (counter), str(attrName), ']')
    argString += "%s'%s' '%s'%s" % ('[', "properties_%i:value" % (counter), str(attrValue), ']')
    counter += 1
  return argString

#-----

def createBinding(binding, bindingType, attributes):
  if bindingType == "SCAImportWSBinding":
     setSCAImportWSBinding(attributes) 
  elif bindingType == "GeneralClientPolicySet":
     setGeneralClientPolicySet(attributes)
  elif bindingType == "ApplicationClientPolicySet":
     attributes['policySet']
     if policySetExists(attributes['policySet'], 'application'):
       setApplicationClientPolicySet(attributes)
     else:
       raise ValueError('policySet does not exists:' , attributes['policySet'])
  elif bindingType == "WebModContextRoot":
     setWebModContextRoot(attributes)
  elif bindingType == "WSClientBindings":
     setWSClientBindings(attributes)
  elif bindingType == "ModuleProperty":
     setModuleProperty(attributes)
  elif bindingType == "JNDIforEJBnonMDB":
     setJNDIforEJBnonMDB(attributes)
  elif bindingType == "SCAImportHttpBindingSSLConfiguration":
     setSCAImportHttpBindingSSLConfiguration(attributes)
  elif bindingType == "SCAImportHttpBindingWithAuth":
     setSCAImportHttpBindingWithAuth(attributes)
  elif bindingType == "SCAImportHttpBinding":
     setSCAImportHttpBinding(attributes)
  elif bindingType == "SCAImportBindingProxy":
     setSCAImportBindingProxy(attributes)
  elif bindingType == "SCAImportHttpBindingConnectionRetries":
     setSCAImportHttpBindingConnectionRetries(attributes)
  elif bindingType == "DestinationMaxRetries":
     setDestinationMaxRetries(attributes)
  elif bindingType == "MDBRetries":
     setMDBRetries(attributes)
  elif bindingType == "SharedLibraryForModule":
     setSharedLibraryForModule(attributes)
  elif bindingType == "ActivationSpecMaxConcurrency":
     setActivationSpecMaxConcurrency(attributes)
  else:
     print "Binding Type Not Recognized"
