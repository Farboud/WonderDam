#WonderDam
#A program to study the storage and releases of a reservoir.

from operator import add
from input import file_input
from calc import wonderland
from inflow import arma_model
from need import Bookan_Need
from properties import res_prop
from optimization import hedge, index, sop
from output import file_output
from curve import rule_curve
from formula import regression

def main():
	number_of_iterations=100
	years=51
	# Read input data from the input file
	(y,k,n,p,tr,scenario,noise)=file_input("input.txt")
	
	# Run wonderland based on the input data
	if noise==False:
		(y,n,k,p,years)=wonderland(years,y,k,n,p,tr,scenario,noise,number_of_iterations)
		
		#since noise can make the results unpredictable, the average of
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
		for counter in range (0,iterations):
			(y,n,k,p,years)=wonderland(years_init,y_init,k_init,n_init,p_init,tr,scenario,noise,number_of_iterations)
			for c in range(0,years_init):
				n_avg[c]=n_avg[c]+n[c]/iterations
#		print(n_avg)
	number_of_years=years[len(years)-1]
	
	# Determine inflow
	#len=100*(number of years)*12
	inflow=arma_model('inflow_series.csv',number_of_iterations)
	
	#determine the need
	need=Bookan_Need(number_of_years,n,number_of_iterations)
	
	#reservoir properties
	properties=res_prop("Bookan")
	
	# Output inflow and need to file
# Since the file outputs are rather large (about 1MB) and their data is
# not really needed, outputs are not written to files.
# Uncomment the next line if you need more data.
#	file_output("out.txt",scenario,k[0],tr,inflow,need,properties)

	# Determine releases (Hedging)
	storage,release,deficit=hedge(inflow,need,properties)
	
	# Determine releases (SOP)
	# If you want SOP, comment out line 63 and uncomment the next line
#	storage,release,deficit=sop(inflow,need,properties)
	
	# Indices
	reliability, resilience, vulnerability, si, msi=index(inflow,need,storage,release,deficit)
	
	# Rule Curve
	rule_curve(release,"Release",si,msi,vulnerability)
	rule_curve(storage,"Storage",si,msi,vulnerability)
	
	# Multivariate Regression
	formula=regression(release,inflow,need,storage)
	
	
	
if __name__ == "__main__":
    main()
    
