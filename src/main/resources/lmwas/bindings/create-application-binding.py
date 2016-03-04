#Add each of the different bindings to their respective modules
if hasattr(deployed, 'bindings'):
	primary = []
	secondary = []
	for binding in deployed.bindings:
		if binding.bindingOrder == 1:
			primary += [binding]
		elif binding.bindingOrder == 2:
			secondary += [binding]
	for binding in primary:
		createBinding(deployed.name, binding.bindingType, bindingAsHash(binding))
	for binding in secondary:
		createBinding(deployed.name, binding.bindingType, bindingAsHash(binding))	
