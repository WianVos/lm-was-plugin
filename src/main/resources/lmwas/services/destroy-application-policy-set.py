if policySetExists(deployed.name, 'application'):
	print "%s exists" % deployed.name
	AdminTask.deletePolicySet(['-policySet', deployed.name])

