#optimization.py
#Routine to optimize reservoir release
#One point Hedging rules are used

import matplotlib.pyplot as plt

def area_by_storage(s,p,i,q,j,k):
	area=p*(s**i)+q*(s**j)+k
	return area

def hedge(inflow,demand,properties):
	evapr_m,mins,maxs,inits,p,i,q,j,k=properties
	
	# make evaporation the same length as inflow
	evap=[]
	for index in range(0,int(len(inflow)/12)):
		evap.extend(evapr_m)
	
	# usable storage
	max_s_usable=maxs-mins
	# minimum storage is considered to be zero
	# dead storage is added at the end
	storage=[0]*(len(inflow)+1)
	release=[0]*len(inflow)
	deficit=[0]*len(inflow)
	storage[0]=inits-mins
	
	for month in range(0,len(inflow)):
		evaporation=evap[month]*area_by_storage(storage[month],p,i,q,j,k)
		wa=storage[month]+inflow[month]-evaporation
		wa_max=max_s_usable+demand[month]
		# Hedging Rules
		# first estimation of release
		#b as in ax^2+bx+c=0
		b=(storage[month]+inflow[month]-evaporation)
		if (b*b-4*b)<0:
			# hedging can't be optimized
			# sop is used
			if demand[month]>storage[month]+inflow[month]:
				release[month]=storage[month]+inflow[month]
			elif demand[month]<storage[month]+inflow[month] and storage[month]+inflow[month]<max_s_usable:
				release[month]=demand[month]
			else:
				release[month]=storage[month]+inflow[month]-max_s_usable
		else:
			r=-1*b-((b*b-4*b)**(0.5))/(-2)
			s_t_plus_1=storage[month]+inflow[month]-evaporation-r
			r_star=wa*demand[month]/(s_t_plus_1+demand[month])
			#release based on hedging rules
			if wa<(s_t_plus_1+inflow[month]-evaporation-r+demand[month]):
				release[month]=r_star
			elif wa>=(s_t_plus_1+inflow[month]-evaporation-r+demand[month]) and wa<=wa_max:
				release[month]=demand[month]
			elif wa>wa_max:
				release[month]=storage[month]+inflow[month]-max_s_usable
			else:
				release[month]=0
			
			if release[month]<0:
				release[month]=0
		if release[month]<demand[month]:
			deficit[month]=demand[month]-release[month]
		else:
			deficit[month]=0
			
		# storage
		storage[month+1]=storage[month]+inflow[month]-evaporation-release[month]
		
		# Extra Spill in case the reservoir capacity exceeds the limit
		if storage[month+1]>max_s_usable:
			release[month]+=(storage[month+1]-max_s_usable)
			storage[month+1]=max_s_usable
		
	storage=storage[:len(inflow)]
	
	for index in range(0,len(storage)):
		storage[index]+=mins
	
	return storage,release,deficit

def sop(inflow,demand,properties):
	evapr_m,mins,maxs,inits,p,i,q,j,k=properties
	
	# make evaporation the same length as inflow
	evap=[]
	for index in range(0,int(len(inflow)/12)):
		evap.extend(evapr_m)
	
	# usable storage
	max_s_usable=maxs-mins
	# minimum storage is considered to be zero
	# dead storage is added at the end
	storage=[0]*(len(inflow)+1)
	release=[0]*len(inflow)
	deficit=[0]*len(inflow)
	storage[0]=inits-mins
	
	for month in range(0,len(inflow)):
		evaporation=evap[month]*area_by_storage(storage[month],p,i,q,j,k)
		if demand[month]>storage[month]+inflow[month]:
			release[month]=storage[month]+inflow[month]
		elif demand[month]<storage[month]+inflow[month] and storage[month]+inflow[month]<max_s_usable:
			release[month]=demand[month]
		else:
			release[month]=storage[month]+inflow[month]-max_s_usable
			
			if release[month]<=0:
				release[month]=0
		if release[month]<=demand[month]:
			deficit[month]=demand[month]-release[month]
		else:
			deficit[month]=0
			
		# storage
		storage[month+1]=storage[month]+inflow[month]-evaporation-release[month]
		
		# Extra Spill in case the reservoir capacity exceeds the limit
		if storage[month+1]>max_s_usable:
			release[month]+=(storage[month+1]-max_s_usable)
			storage[month+1]=max_s_usable
		
	storage=storage[:len(inflow)]
	
	for index in range(0,len(storage)):
		storage[index]+=mins
	
	return storage,release,deficit

def index(inflow,demand,storage,release,deficit):

	# Reliability
	not_reliable=0
	for month in range(0,len(demand)):
		if demand[month]>release[month]:
			not_reliable+=1
	reliability=100*(1-not_reliable/len(demand))
	
	# Resilience
	resilient=0
	num_d_ge_r=0
	for month in range(0,len(demand)-1):
		if demand[month]>release[month]:
			num_d_ge_r+=1
			if demand[month+1]<=release[month+1]:
				resilient+=1
	resilience=100*resilient/num_d_ge_r
	
	# Vulnerability
	vulnerability=0
	for month in range(0,len(demand)):
		if demand[month]>release[month]:
			rel_def=(demand[month]-release[month])/demand[month]
			vulnerability=max(vulnerability,rel_def)
	vulnerability*=100
	if vulnerability>100:
		vulnerability=100
	
	# Shortage Index (SI)
	relative_deficit_2=0
	for month in range(0,len(demand),12):
		annual_deficit= deficit[month:month+12]
		annual_deficit=	sum(annual_deficit)
		annual_demand= demand[month:month+12]
		annual_demand=	sum(annual_demand)
		relative_deficit_2+=(annual_deficit/annual_demand)**2
	years=len(demand)/12
	si=100*relative_deficit_2/years
	
	# Modified Shortage Index (MSI)
	ts_td=0
	for month in range(0,len(demand)):
		ts_td+=(deficit[month]/demand[month])**2
	msi=100*ts_td/len(demand)
	
	return reliability, resilience, vulnerability, si, msi
		
