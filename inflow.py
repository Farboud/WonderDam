#inflow.py
# module to generate future monthly inflow for Bookan dam using ARMA method
# based on data provided by Urmia Lake Restoration Program (ULRP)
from pandas import read_csv
from pandas import datetime
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARMAResults
import statsmodels.api as sm
import numpy as np

def parser(x):
	return datetime.strptime(x, '%y-%m')
	
def arma_model(in_filename,number_of_iterations):

# Read Dataset
	series = read_csv(in_filename, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
# Returns information criteria for ARMA models
	order_aic = sm.tsa.arma_order_select_ic(series, ic=['aic'], trend='c').aic_min_order

# Develop ARMA Model
# http://www.statsmodels.org/dev/generated/statsmodels.tsa.arima_model.ARMA.html
# http://www.statsmodels.org/dev/generated/statsmodels.tsa.arima_model.ARMA.fit.html
	armamodel=ARMA(series, order_aic).fit(transparams=True,trend='c')
	
# ARMA Parameters
# http://www.statsmodels.org/dev/generated/statsmodels.tsa.arima_model.ARMA.predict.html
	res=ARMAResults.predict(start=1, end=len(series), dynamic=False, self=armamodel)

# Noise Inclusion
	mean=0
	std=1
	num_samples=len(res)
	
	inflow=[]
	for i in range(0,number_of_iterations):
		noise=np.random.normal(mean,std,size=num_samples)
		res1=res+noise
# Replace Negative Values With Zero
		for index in range(0,len(res1)):
			if res1[index]<0:
				res1[index]=0
		inflow.extend(res1)
# Return	
	return(inflow)
