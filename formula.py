#formula.py
#Routine to develop regression formulas for release

import numpy as np
import statsmodels.api as sm

def sort_by_month(in_list):
#keeps the values of each month in a seperate list
	out=[]*12
	for month in range(0,12):
		out_month=[]
		for i in range(month,len(in_list),12):
			out_month.append(in_list[i])
		out.append(out_month)
	return out

def regression(release,inflow,demand,storage):
	for month in range(0,12):
		release_month=sort_by_month(release)[month]
		inflow_month=sort_by_month(inflow)[month]
		demand_month=sort_by_month(demand)[month]
		storage_month=sort_by_month(storage)[month]
		x=[]
		for index in range(0,len(release_month)):
			x_index=[inflow_month[index],demand_month[index],storage_month[index]]
			x.append(x_index)
		y=release_month
		x=np.array(x)
		y=np.array(y)

		X = np.insert(x, 0, np.ones((1,)), axis=1)
		
		months=["Mehr","Aban","Azar","Dey","Bahman","Esfand","Farvardin","Ordibehesht","Khordad","Tir","Mordad","Shahrivar"]
		
		print("------------------------------------------------------------------------------")
		print(months[month])
		print("------------------------------------------------------------------------------")
		print(sm.OLS(y, X).fit().summary())
		print("Press to continue")
		dummy=input()
