def policySetExists(name, policySetType):
  policysets = AdminTask.listPolicySets(['-policySetType', policySetType]).splitlines()

  for s in policysets:
   if name == s :
    print "policy set %s exists" % name
    return True
 
  print "policy set %s does not exists" % name 
  return False  
#------
def createPolicySet(name, description, type):
  AdminTask.createPolicySet(['-policySet', name , '-description', description,'-policySetType', type]) 
  print "created policy set %s" % name
#------
def containsPolicyType(policyName, type):
  policytypes = AdminTask.listPolicyTypes(['-policySet', policyName]).splitlines()	
  for t in policytypes:
   if type == t:
    print "policy %s contains type %s" % (policyName, type)
    return True
  
  return False
  print "policy %s does not contain type %s" % (policyName, type)
#------
def customizePolicySetType(policysetname, type, attribName, attribValue):
  AdminTask.setPolicyTypeAttribute(['-policySet', policysetname, '-policyType', type, '-attributeName', attribName ,'-attributeValue', attribValue ])
  print "updated %s : %s with %s = %s" % (policysetname, type, attribName, attribValue)
#------
def addPolicySetType(policysetname, type):
  AdminTask.addPolicyType(['-policySet', policysetname, '-policyType', type,'-enabled', 'true'])
  print "added %s to policyset %s" % (type, policysetname)
#------
def updatePolicySetSettings(policysetname, type, settings):
 if not containsPolicyType(policysetname, type):
  addPolicySetType(policysetname, type)
 if len(settings) > 0:
  for key, value in tuple(settings.items()):
   customizePolicySetType(policysetname, type, key, value)
#------
def setApplicationClientPolicySet (appName, provider, policySet, webModuleName, namespace, WebServiceClient):

    print " Setting " + provider + "  PolicySet for webservice " + WebServiceClient + " to: " + policySet

    AdminTask.createPolicySetAttachment("-applicationName %s -attachmentType %s -policySet %s -resources [WebService:/%s:{%s}%s ]" % (appName, provider, policySet, webModuleName, namespace, WebServiceClient))
#-----
def policyAttachmentExists(policySet, application):
  attachments = AdminTask.listAttachmentsForPolicySet(['-policySet', deployed.policySet ]).splitlines()

  for a in attachments:
   if application == a :
     print "policy set %s is attached to %s" % (policySet, application)
     return True
   print "policy set %s is NOT attached to %s" % (policySet, application)
   return False

#--- new style

def toEnclosedAttrString(attributes, startChar, endChar):
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

#---
def booleanArguments():
  return ['acceptRedirectedURL','maintainSession', 'chunkTransferEnc', 'sendExpectHeader', 'messageResendOnce', 'persistConnection', 'allowTransactionalAsyncMessaging', 'inResponseSSLenabled', 'outAsyncResponseSSLenabled', 'outRequestSSLenabled', 'inOrderDelivery']

#---
def normalizeValues(value, name):
 if value == "true": 
  value="yes"
 if value == "false":
  value="no"
 for arg in booleanArguments():
  if name == arg:
   if str(value) == "0":
    value="no"
   elif str(value) == "1":
    value="yes"

 return value
#---  
def policyAsHash(policy):
  unwantedProperties = ['container','deployable','id', 'name', 'policyType','type']
  returnHash = {}
  for property in policy._properties:
    if property not in unwantedProperties:
      if isinstance(getattr(policy, property), DictionaryObject):
        if property == "customProperties":
          returnHash[property] = getattr(policy, property)
        else:
          returnHash[str(getattr(policy,property).name)] = str(getattr(policy,property).value)
      else:
        returnHash[property] = normalizeValues(getattr(policy, property), property)

  return returnHash

#----

def customPropertiesToEnclosedAttrString(attributes):
  argString = ""
  counter = 0 
  for attrName, attrValue in attributes.items():
    argString += "%s'%s' '%s'%s" % ('[', "properties_%i:name" % (counter), str(attrName), ']')
    argString += "%s'%s' '%s'%s" % ('[', "properties_%i:value" % (counter), str(attrValue), ']')
    counter += 1
  return argString 

#----

def createPolicy(policySet, policyType, attributes):
  
  addPolicySetType(policySet, policyType)
  
  try:
    print AdminTask.setPolicyType("-policySet %s -policyType %s -attributes %s" % (policySet, policyType, attributes))
    print "created policyType %s for policySet %s with attributes: %s" % (policyType, policySet, attributes)
  except:
    print "unable to create policy type: %s for policyset %s" % (policyType, policySet)
    raise
#----
def createClientPolicySetBindingPolicy(setName, policyType, attachmentType, bindingScope, attributes):

  try:
    print AdminTask.setBinding("-policyType %s -attachmentType %s -bindingScope %s -attributes %s -bindingName %s -bindingLocation" % (policyType, attachmentType, bindingScope, attributes, setName))
    print "created policyType %s for policySet %s with attributes: %s" % (policyType, setName, attributes)
  except:
    print "unable to create policyBinding type: %s for policyBindingSet %s" % (policyType, setName)
    raise


def destroyClientPolicySetBindingPolicy(setName, attachmentType):
  try:
    print AdminTask.setBinding("-bindingLocation -attachmentType %s -remove true -bindingName %s" % (attachmentType, setName))
    print "removed policySet %s" % (setName)
  except:
    print "unable to remove policyBindingClientThingy %s" % (setName)
    raise

def createClientPolicySetBinding(deployed):
  if hasattr(deployed, 'policies'): 
   for policy in deployed.policies:
    createClientPolicySetBindingPolicy( deployed.name, policy.policyType, deployed.attachmentType, deployed.bindingScope, toEnclosedAttrString(policyAsHash(policy),'[',']')  )
  else:
   print "policyset %s has no binding policies assigned to it .. and will therefore not be created" % (deployed.name)    

def createClientPolicySetBindingAttachement(bindingName, attachmentType, applicationName, serviceName):

  output = AdminTask.getPolicySetAttachments('[-applicationName %s -attachmentType client]' % (applicationName)).replace(' ','=').replace(']=[',';').replace('[=[','').replace(']=]','')
  print output
  adDict = {}
  for x in output.split(';'):
   key, value = x.split('=') 
   adDict[key] = value
   

  try:
    print AdminTask.setBinding("-bindingScope domain -bindingName %s -attachmentType %s -bindingLocation [ [application %s] [attachmentId %s] ]" % (bindingName, attachmentType, applicationName, adDict['id']))
    print "attached %s to application: %s" % (bindingName, applicationName) 
  except:
    print "unable to attach %s to application: %s" % (bindingName, applicationName)
    raise
