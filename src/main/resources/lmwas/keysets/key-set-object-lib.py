def keySetExists(dynamicName, scopeName):
     for domain in AdminTask.listKeySets().splitlines():
          if domain == dynamicName:
               print "Key set %s Exists" % dynamicName
               return True
          else:
               print "Config name: %s" % dynamicName

def destroyKeySet(dynamicName, scopeName):
     print "Destroying key set %s" % dynamicName
     AdminTask.deleteKeySet(['-name', dynamicName, '-scopeName', scopeName])

def populateManagementScope(target, name, cellname):
     mgtScope = "(cell):" + cellname +":(" + target "):" + name
     print "Populated management scope: " + mgtScope
     return mgtScope
     
def populateConfigScope(cellname):
     cellScope = "(cell):" + cellname
     print "Populated cell scope: " + cellScope
     return cellScope
