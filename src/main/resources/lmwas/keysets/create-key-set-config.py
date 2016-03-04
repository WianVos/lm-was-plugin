# check for if the configuration exists and if it does, start over
if keySetExists(deployed.name, deployed.managementScope):
     destroyKeySet(deployed.name)

# retrieve management scope
mgtScope = populateManagementScope(deployed.container.wasTargetType, deployed.container.name, deployed.container.cellName) 

confScope = populateConfigScope(deployed.container.cellName)

AdminTask.createKeySet(['-name', deployed.name , '-scopeName', mgtScope, '-aliasPrefix', deployed.prefix, '-password', deployed.password,'-maxKeyReferences', deployed.maxKeys,'-isKeyPair', deployed.isKeyPair, '-keyGenerationClass', deployed.keyGenClass, '-keyStoreName', deployed.keyStoreName, '-keyStoreScopeName', deployed.keyStoreName]) 

