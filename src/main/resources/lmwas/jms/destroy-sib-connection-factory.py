#

id = AdminConfig.getid('/J2CConnectionFactory:%s' % (deployed.name))
if id == "":
    print >> sys.stderr, "Cannot find SIB Connection Factory", deployed.name
    sys.exit(1);

print "Destroying SIB Connection Factory %s" %(deployed.name)
AdminConfig.remove(id)
 
