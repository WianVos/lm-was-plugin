
def getJaasAuthenticationDataArgs(deployed):
    exposedProperties = deployed.getExposedProperties(True)
    exposedProperties['alias'] = deployed.objectName
    exposedProperties['userId'] = deployed.username
    del exposedProperties['objectName']
    args = toAdminConfigArgs(exposedProperties)
    return args

def findJaasAuthenticationData(aliasName, cellName):
    """ find jaas authentication data in global security. """
    securityId = AdminConfig.getid("/Cell:%s/Security:/" % cellName)
    jaasAliases = wsadminToList(AdminConfig.list('JAASAuthData', securityId))
    jaasAliasList = [ja for ja in jaasAliases if AdminConfig.showAttribute(ja, 'alias') == aliasName]

    if jaasAliasList:
        return jaasAliasList[0]
    return None

def jaasAuthenticationDataExists(deployed):
    return findJaasAuthenticationData(deployed.objectName, deployed.container.cellName) is not None

def createJaasAuthenticationData(deployed):
    securityId = AdminConfig.getid("/Cell:%s/Security:/" % deployed.container.cellName)
    args = getJaasAuthenticationDataArgs(deployed)
    AdminConfig.create('JAASAuthData', securityId, args)

def modifyJaasAuthenticationData(deployed):
    args = getJaasAuthenticationDataArgs(deployed)
    aliasId = findJaasAuthenticationData(deployed.objectName, deployed.container.cellName)
    AdminConfig.modify(aliasId, args)

def destroyJaasAuthenticationData(jaasAliasName, cellName):
    jaasAlias = findJaasAuthenticationData(jaasAliasName, cellName)
    if jaasAlias:
        AdminConfig.remove(jaasAlias)
        return True
    else:
        return False
