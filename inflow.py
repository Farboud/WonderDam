#inflow.py
#module to create future monthly or annual inflow for Bookan dam
#based on data provided by Urmia Lake Restoration Program (ULRP)
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

def parser(x):
	return datetime.strptime(x, '%y-%m')
 
 
def arima_model(input_file,autoreg,stationary,m_avg,predic_years):
	series = read_csv(input_file, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

	X = series.values
	size = int(len(X) * 0.66)
	train, test = X[0:size], X[size:len(X)]
	history = [x for x in train]
	predictions = list()
	for t in range(len(test)):
		model = ARIMA(history, order=(autoreg,stationary,m_avg))
		model_fit = model.fit(disp=0)
		output = model_fit.forecast()
		yhat = output[0]
		predictions.append(yhat)
		obs = test[t]
		history.append(obs)
		print('predicted=%f, expected=%f' % (yhat, obs))
	
	for i in range(0,len(predictions)):
		if predictions[i]<0:
			predictions[i]=0
	error = mean_squared_error(test, predictions)
	print('Test MSE: %.3f' % error)
	
	output=[]
	for item in predictions[-1*predic_years*12:]:
		output.append(item[0])
		
	return output

def Bookan_Inflow(time,freq,sc,input_file,autoreg,stationary,mov_avg):
#arguments are desired time length, monthly or annual data and scenario
#time is an integer
#for monthly enter 'm' and for annual enter 'a'
#scenarios are 'nochange' and 'trend' and 'arima'
	month_avg=[9.60,37.36,61.98,75.60,103.14,198.19,363.54,250.46,
	58.60,19.19,12.47,9.64]
	year_avg=1199.77
	if sc=='arima':
		inflow=arima_model(input_file,autoreg,stationary,mov_avg,time)
	else:
		if sc=="nochange":
			m=0
		elif sc=="trend":
			m=-0.24
		if freq=='a':
			inflow=[]*time
		elif freq=='m':
			inflow=[]*(time*12)
		for t in range(0,time):
			if freq=='a':
				current_year_avg=(t*m)+year_avg
				inflow.append(current_year_avg)
			if freq=='m':
				change=t*m
				current_month_avg=[0]*12
				for j in range(0,11):
					current_month_avg[j]=change+month_avg[j]
					if current_month_avg[j]<0:
						inflow.append(0)
					else:
						inflow.append(current_month_avg[j])
				current_month_avg[11]=change+month_avg[11]
				if current_month_avg[11]<0:
					inflow.append(0)
				else:
					inflow.append(current_month_avg[11])
	return inflow
	
