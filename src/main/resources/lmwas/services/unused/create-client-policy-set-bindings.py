# policyTypeNames = ['JMSTransport','HTTPTransport','CustomProperties','SSLTransport','WSReliableMessaging', 'WSSecurity']

# # create the policySet if it does not exists
# # add the subsets to the policy in accordance with the specification
# for policyType in policyTypeNames:
#  exec('includePolicy=deployed.include%s') % policyType
#  settingsVarName = 'deployed.'+policyType+'Settings'
#  exec('settings=%s') % settingsVarName
 
#  for key, value in tuple(settings.items()):
#   AdminTask.setBinding("-policyType %s -bindingScope domain -attributes [[%s %s]] -bindingName %s -bindingLocation" % (policyType, key, value, deployed.name))
# create the policySet if it does not exists

#create general client policy set binding



#Create and/or update to policies
print dir(deployed)
    
bla

#AdminTask.setPolicyType('[-policySet Test1_Xldeploy -policyType HTTPTransport -attributes [ [acceptRedirectedURL yes] [readTimeout 300] [maintainSession yes] [protocolVersion HTTP/1.1] [chunkTransferEnc yes] [sendExpectHeader Yes] [compressRequest:name none] [compressResponse:name none] [messageResendOnce no] [connectTimeout 180] [writeTimeout 300] [persistConnection yes] ]]') 
