#output.py
#Routine to read wonderland parameters from input file
def file_output(path,scenario,k,tr,inflow,need,properties):
#	path = 'out.txt'

	output_file = open(path,'w')
#Model Information
	output_file.write("Scenario="+str(scenario)+" Reserves="+str(k)+\
	" Tax_Rate="+str(tr))

#Planning time
	years=int(len(inflow)/12)
	output_file.write("\n\nNumber of Years:\n")
	output_file.write(str(years))
	
#Inflows
	output_file.write("\n\nDam Inflows:\n")
	counter=0
	for flow in inflow[len(inflow)%12:]:
		output_file.write(str("%.2f" % flow))
		counter+=1
		if counter!=len(inflow)-len(inflow)%12:
			output_file.write(",")
#Needs
	output_file.write("\n\nWater Needs:\n")
	counter=0
	for usage in need[:int(len(inflow)/12)*12]:
		output_file.write(str("%.2f" % usage))
		counter+=1
		if counter!=int(len(inflow)/12)*12:
			output_file.write(",")
#Evaporation
	output_file.write("\n\nEvaporation:\n")
	counter=0
	for year in range(0,int(len(inflow)/12)+1):
		for evap in properties[0]:
			output_file.write(str("%.1f" % evap))
			counter+=1
			if counter!=int((len(inflow)/12)):
				output_file.write(",")
#Storage
	output_file.write("\n\nReservoir Minimum Operational Storage:\n")
	output_file.write(str("%.1f" % properties[1]))
	
	output_file.write("\n\nReservoir Maximum Operational Storage:\n")
	output_file.write(str("%.1f" % properties[2]))

	output_file.write("\n\nReservoir Initiating Storage:\n")
	output_file.write(str("%.1f" % properties[3]))
#reservoir Area by its Storage
	output_file.write("\n\np:\n")
	output_file.write(str(properties[4]))
	output_file.write("\n\ni:\n")
	output_file.write(str("%.1f" % properties[5]))
	output_file.write("\n\nq:\n")
	output_file.write(str("%.4f" % properties[6]))
	output_file.write("\n\nj:\n")
	output_file.write(str("%.1f" % properties[7]))
	output_file.write("\n\nk:\n")
	output_file.write(str(properties[8]))

	output_file.close()
