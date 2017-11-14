#need.py
#module to create future monthly or annual inflow for Bookan dam
#based on data provided by Urmia Lake Restoration Program (ULRP)


def Bookan_Need(time,pop):
#arguments are desired time length, monthly or annual data and scenario
#time is an integer
#for monthly enter 'm' and for annual enter 'a'
#scenarios are 'nochange' and 'trend'
	env_need=[44.4]*12
	current_need=[32.6,12.3,5.7,5.1,5.9,9.1,23.1,33.3,57.7,71.5,76.4,56.3]
#	need=[0]*(12*time)
	need=[]
	for i in range(0,time):
		this_year_need=[0]*12
		for j in range(0,12):
			this_year_need[j]=current_need[j]*pop[i]+env_need[j]
			need.append(this_year_need[j])
	return need
	
