if hasattr(deployed, 'bindings'):
  for binding in deployed.bindings:
    if binding.bindingType == "ApplicationClientPolicySet" and policyAttachmentExists(binding.policySet, binding.applicationName):
	  AdminTask.deleteAttachmentsForPolicySet(['-policySet', binding.policySet, '-applicationName', binding.applicationName])
          print "attachement %s for policyset %s destroyed" % (binding.applicationName, binding.policySet)

print "Module bindings will be removed when module spec is rolled back"
print "General Client Bindings are going to be detached when the Application policy set attachement is rolled back"
