if policyAttachmentExists(deployed.policySet, deployed.applicationName):
  AdminTask.deleteAttachmentsForPolicySet(['-policySet', deployed.policySet, '-applicationName', deployed.applicationName])  
  print "attachement %s for policyset %s destroyed" % (deployed.applicationName, deployed.policySet)
