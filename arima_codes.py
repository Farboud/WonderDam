
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

# plot
#	pyplot.plot(test, color ='blue', label='Observed Data')
#	pyplot.plot(predictions, color='red', label='Predicted Data')
#	pyplot.title("ARIMA Model")
#	pyplot.xlabel("Time (Months)")
#	pyplot.ylabel("Inflow (MCM)")
#	axes = pyplot.gca()
#	axes.set_xlim([0,len(predictions)])
#	pyplot.legend()
#	pyplot.show()



