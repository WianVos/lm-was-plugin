#Add each of the different bindings to their respective modules
if hasattr(deployed, 'bindings'):
	primary = []
	secondary = []
	for binding in deployed.bindings:
                print binding
		if binding.bindingOrder == 1:
			primary += [binding]
		elif binding.bindingOrder == 2:
			secondary += [binding]
	for binding in primary:

		output = createBinding(deployed.name, binding.bindingType, bindingAsHash(binding))
                print output

	for binding in secondary:
		output = createBinding(deployed.name, binding.bindingType, bindingAsHash(binding))	
                print output
