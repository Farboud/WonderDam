#input.py
#Module to read wonderland parameters from input file
def file_input(path):
#	path = 'input.txt'
	input_file = open(path,'r')
	input_contents= input_file.readlines()
	years=int(input_contents[0].split()[1])
	y=float(input_contents[1].split()[1])
	k=float(input_contents[2].split()[1])
	n=float(input_contents[3].split()[1])
	p=float(input_contents[4].split()[1])
	tr=float(input_contents[5].split()[1])
	scenario=str(input_contents[6].split()[1]).lower()
	noise=bool(input_contents[7].split()[1])
	inflow_scenario=str(input_contents[8].split()[1]).lower()
	
	autoreg=int(input_contents[9].split()[1])
	stationary=int(input_contents[10].split()[1])
	mov_avg=int(input_contents[11].split()[1])
	input_file.close()
	return(years,y,k,n,p,tr,scenario,noise,inflow_scenario,autoreg,stationary,mov_avg)
