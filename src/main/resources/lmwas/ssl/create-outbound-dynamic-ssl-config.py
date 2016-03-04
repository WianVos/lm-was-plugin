# retrieve management scope
mgtScope = populateManagementScope(deployed.container.wasTargetType, deployed.container.name, deployed.container.cellName) 

# retrieve config scope
confScope = populateConfigScope(deployed.container.cellName)

# check for if the configuration exists and if it does, start over
if dynamicSSLConfigExists(deployed.name, mgtScope):
     destroyDynamicSSLConfig(deployed.name)

connectList = configureList(deployed.connectionInformation)
     
# create the dynamic ssl config
AdminTask.createDynamicSSLConfigSelection(['-dynSSLConfigSelectionName', deployed.name, '-scopeName', mgtScope, '-dynSSLConfigSelectionDescription', deployed.description, '-dynSSLConfigSelectionInfo', connectList, '-sslConfigName', deployed.sslConfiguration, '-sslConfigScope', confScope, '-certificateAlias', deployed.certificateAlias])

