parent = AdminConfig.getid(deployed.container.containmentPath)
args = toAdminTaskArgs(deployed.getExposedProperties())
args.extend(['-type', deployed.sibType])

print "Creating SIB connection factory on target scope %s with args %s" %(parent, args)
AdminTask.createSIBJMSConnectionFactory(parent, args)
