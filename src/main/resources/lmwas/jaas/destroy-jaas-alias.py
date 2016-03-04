if destroyJaasAuthenticationData(deployed.objectName, deployed.container.cellName):
    print "Destroyed JAAS/J2C authentication data '%s'" % (deployed.objectName)
else:
    print "No JAAS/J2C authentication data '%s'. Nothing to do." % (deployed.objectName)
