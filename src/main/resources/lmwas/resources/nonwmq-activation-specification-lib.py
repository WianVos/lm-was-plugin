def asExists(deployed):
  for as in wsadminToList(AdminTask.listSIBJMSActivationSpecs(AdminConfig.getid(deployed.container.containmentPath))):
    if as[:as.find("(")] == deployed.name:
     return True
  return False

def asDestroy(as):
 try:
  AdminTask.deleteSIBJMSActivationSpec(as)
  print "JMSActivation spec %s deleted" % (as)
 except:
  raise "JMSActivation spec %s found , but could not be deleted.. " % (as)

def getId(deployed):
 for as in wsadminToList(AdminTask.listSIBJMSActivationSpecs(AdminConfig.getid(deployed.container.containmentPath))):
  if as[:as.find("(")] == deployed.name:
   return as
  else:
   print "id not found"

def createJMSActivationSpec(deployed):
  containerId = AdminConfig.getid(deployed.container.containmentPath)
  arguments = getCommandArguments(deployed)
  try:
    print AdminTask.createSIBJMSActivationSpec(containerId, arguments)
    print "created JMS activation specification: %s" % (deployed.name)
    print "scope: %s " % (containerId)
    print "with arguments: %s " % (arguments)
  except:
    print "failed to create JMS activation specification: %s" % (deployed.name)

def getCommandArguments(deployed):
  arguments = ""
  for arg in commandArguments():
    if hasattr(deployed, arg):
      if hasattr(deployed, "%s_as_string" % (arg)):
       arguments += "-%s %s " % (arg, getattr(deployed,  "%s_as_string" % (arg)))
      else:
       if str(type(getattr(deployed, arg))) == 'org.python.core.PyInteger':
        arguments += "-%s %s " % (arg, getattr(deployed,  "%s" % (arg)))
       elif getattr(deployed,  "%s" % (arg)):
        arguments += "-%s %s " % (arg, getattr(deployed,  "%s" % (arg)))
       else:
        arguments += "-%s "  % (arg)
  return arguments

