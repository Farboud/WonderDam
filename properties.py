#properties.py
#Routine to return reservoir properties
#Since we are only studying one reservoir, this does not do anything
#	of interest and only return the given parameters.
def res_prop(dam):
	#reservoir Area-Volume curve (mm/month)
	evap=[72.3,35,16.3,14.6,16.7,25.9,65.5,94.5,127.4,154.6,154.6,121.7]
	#A(s(t))=P*S^i+Q*S^j+k
	p=3.772e-11
	i=2
	q=0.092
	j=1
	k=3.476e6
	
	#Storage Volumes (MCM)
	total_vol=762
	normal_vol=650
	practical_vol=486
	mins=(total_vol-practical_vol)
	maxs=762
	#it is assumed the reservoir is half empty
	inits=max(maxs/2,mins)
	return (evap,mins,maxs,inits,p,i,q,j,k)
