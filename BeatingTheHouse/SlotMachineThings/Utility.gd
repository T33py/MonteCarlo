extends Node

func two_decimals(number)-> String:
	'''
	Formats a number with excactly 2 decimals
	'''
	
	var num = str(number)
	var split = num.split(".")
	var ret = split[0] as String
	var dec = ""
	if num.contains("."):
		dec = split[1] as String
		if len(dec) > 2:
			dec = dec.substr(0, 2)
	
		while len(dec) < 2:
			dec += "0"
		
		ret = ret + "." + dec
	
#	print(str(number) + " -> " + ret + "." + dec)
	return ret 
