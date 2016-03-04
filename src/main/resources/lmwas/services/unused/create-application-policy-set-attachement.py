#bind policy set to a webservice and do something usefull. 
# find the resource name for the specified module/application.
if policySetExists(deployed.policySet, 'application'):
  setApplicationClientPolicySet(deployed.applicationName, deployed.attachmentType, deployed.policySet, deployed.webModuleName, deployed.namespace, deployed.serviceName)
else:
  raise ValueError('policySet does not exists:' , deployed.policySet)
