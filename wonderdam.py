#WonderDam
#A program to study the needs and inflows of a dam.

from input import file_input
from calc import wonderland
from inflow import Bookan_Inflow
from need import Bookan_Need
from properties import res_prop
from output import file_output
from operator import add


def main():
	#read input data from the input file
	(years,y,k,n,p,tr,scenario,noise,inflow_scenario,autoreg,stationary,mov_avg)=file_input("input.txt")
	
	#run wonderland based on the input data
	if noise==False:
		(y,n,k,p,years)=wonderland(years,y,k,n,p,tr,scenario,noise)
		
		#since noise can make the results unpredictablr, the average of
		# multiple model runs is used to smoothen the results.
		# Also, we only use 'n' in the later modules, so in order to
		# save processing power, only the average of 'n' is calculated.
		
	if noise==True:
		iterations=5
		#on second thought, since no major change was seen, I lowered
		# the iterations
		years_init=years
		y_init=y
		k_init=k
		n_init=n
		p_init=p
		n_avg=[0]*years_init
		print(years)
		for counter in range (0,iterations):
			(y,n,k,p,years)=wonderland(years_init,y_init,k_init,n_init,p_init,tr,scenario,noise)
			for c in range(0,years_init):
				n_avg[c]=n_avg[c]+n[c]/iterations
		print(n_avg)
	number_of_years=years[len(years)-1]
	
	#determine inflow
	inflow=Bookan_Inflow(number_of_years,'m',inflow_scenario,'inflow_series.csv',autoreg,stationary,mov_avg)
	
	#determine the need
	need=Bookan_Need(number_of_years,n)
	
	#reservoir properties
	properties=res_prop("Bookan")
	
	#output inflow and need to file
	file_output("out.txt",scenario,k[0],tr,inflow_scenario,inflow,need,properties,autoreg)
	
	
if __name__ == "__main__":
    main()
    
