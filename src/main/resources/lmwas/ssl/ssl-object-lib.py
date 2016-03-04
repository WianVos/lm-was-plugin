def dynamicSSLConfigExists(dynamicName, scopeName):
     for domain in AdminTask.listDynamicSSLConfigSelections().splitlines():
          if domain == dynamicName:
               print "Dynamic SSL Config %s Exists" % dynamicName
               return True
          else:
               print "Config name: %s" % dynamicName

def destroyDynamicSSLConfig(dynamicName, scopeName):
     print "Destroying SSL Config %s" % dynamicName
     AdminTask.deleteDynamicSSLConfigSelection(['-dynSSLConfigSelectionName', dynamicName, '-scopeName', scopeName])

def populateManagementScope(target, name, cellname):
     manageScope = "(cell):" + cellname + ":(" + target + "):" + name
     print "Populated management scope: " + manageScope
     return manageScope
     
def populateConfigScope(cellname):
     cellScope = "(cell):" + cellname
     print "Populated cell scope: " + cellScope
     return cellScope

def configureList(list):
     newList = '|'.join(map(str, list))
     return newList
