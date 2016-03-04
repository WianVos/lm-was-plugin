if jaasAuthenticationDataExists(deployed):
    print "Modifying JAAS/J2C authentication data '%s' in container '%s'" % (deployed.objectName, deployed.container.name)
    modifyJaasAuthenticationData(deployed)
else:
    print "Creating JAAS/J2C authentication data '%s' in container '%s'" % (deployed.objectName, deployed.container.name)
    createJaasAuthenticationData(deployed)
