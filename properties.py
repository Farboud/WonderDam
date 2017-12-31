#properties.py
#Routine to return reservoir properties
#Since we are only studying one reservoir, this does not do anything
#	of interest and only return the given parameters.
def res_prop(dam):
	# evaporation rate (mm/month)
	evapr=[72.3,35,16.3,14.6,16.7,25.9,65.5,94.5,127.4,154.6,154.6,121.7]
	# evaporation rate (m/month)
	evapr_m=[0]*len(evapr)
	for index in range(0,len(evapr)):
		evapr_m[index]=evapr[index]/1000
	# A(s(t))=P*S^i+Q*S^j+k
	p=-3.8e-5
	i=2
	q=0.092
	j=1
	k=3.476
	
	# Storage Volumes (MCM)
	total_vol=762
	normal_vol=650
	practical_vol=486
	mins=(total_vol-practical_vol)
	maxs=762
	# it is assumed the reservoir is half empty
	inits=max(maxs/2,mins)
	return (evapr_m,mins,maxs,inits,p,i,q,j,k)
