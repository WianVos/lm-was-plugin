# create the policySet if it does not exists
if not policySetExists(deployed.name, deployed.policySetType):
	createPolicySet(deployed.name, deployed.description, deployed.policySetType)



#Create and/or update to policies
if hasattr(deployed, 'policies'): 
  for policy in deployed.policies:
  	createPolicy(deployed.name, policy.policyType, toEnclosedAttrString(policyAsHash(policy),'[',']') )

