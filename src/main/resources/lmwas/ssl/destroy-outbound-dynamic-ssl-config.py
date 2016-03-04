# retrieve management scope
mgtScope = populateManagementScope(deployed.container.wasTargetType, deployed.container.name, deployed.container.cellName) 

# destroy the configuration
destroyDynamicSSLConfig(deployed.name, mgtScope)
