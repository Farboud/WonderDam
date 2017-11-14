import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np

def sort_by_month(in_list):
#keeps the values of each month in a seperate list
	out=[]*12
	for month in range(0,12):
		out_month=[]
		for i in range(month,len(in_list),12):
			out_month.append(in_list[i])
		out.append(out_month)
	return out

def percentile_x(in_list,percent):
#calculates the given percentile for values of each month
#'in_list' must first be sorted by 'sort_by_month'
	monthly_sorted=sort_by_month(in_list)
	percentile_xx=[]
	for i in range(0,12):
		a = np.array(monthly_sorted[i])
		p = np.percentile(a, percent)
		percentile_xx.append(p)
	return percentile_xx
	
def line_split(file_data,line_num):
	#splits by ',' the given file line into a list
	line=file_data[line_num].split(',')
	out_list=[]
	for datum in line:
		out_list.append(float(datum))
	return out_list
	
def read_results_file(filename):
	pointer=open(filename,'r')

	#Read Data from input file
	raw_data=pointer.readlines()
	data=[]
	for line in raw_data:
		l=line.strip().split('\t')
		data.append(l[0])

	reliability=float(data[1].split(',')[0])
	resiliency=float(data[4].split(',')[0])
	vulnerability=float(data[7].split(',')[0])


	demands=line_split(data,10)
	releases=line_split(data,13)
	inflows=line_split(data,16)
	storage=line_split(data,19)

	return (reliability,resiliency,vulnerability,demands,releases,inflows,storage)

def rule_curve(in_data,title,reliability,resiliency,vulnerability):
	# Rule Curve
	col_labels=['Reliability','Resiliency','Vulnerability']
	table_vals=[[round(reliability,4),round(resiliency,4),round(vulnerability,4)]]
	the_table = plt.table(cellText=table_vals,
					colWidths = [0.14]*3,
					colLabels=col_labels,
					colLoc='center',
					cellLoc='center',
					loc='upper left')
	#percentiles of input
	percentile_0=percentile_x(in_data,0)
	percentile_20=percentile_x(in_data,20)
	percentile_40=percentile_x(in_data,40)
	percentile_60=percentile_x(in_data,60)
	percentile_80=percentile_x(in_data,80)
	percentile_100=percentile_x(in_data,100)	
	#data to be plotted
	one_year=[1,2,3,4,5,6,7,8,9,10,11,12]
	plt.plot(one_year, percentile_0, 'r')
	plt.plot(one_year, percentile_20, 'g')
	plt.plot(one_year, percentile_40, 'b')
	plt.plot(one_year, percentile_60, 'c')
	plt.plot(one_year, percentile_80, 'y')
	plt.plot(one_year, percentile_100, 'm')	
	#labels
	plt.xlabel("Months (Hydrological Year)")
	plt.ylabel("Volume (MCM)")
	plt.title("Reservoir "+title+" Rule Curve")
	#axes limits
	axes = plt.gca()
	axes.set_xlim([1,len(one_year)])
	axes.set_ylim([min(percentile_0)*0.9,max(percentile_100)*1.1])
	#legend definition
	red = mpatches.Patch(color='r', label='Min')
	green = mpatches.Patch(color='g', label='80%')
	blue = mpatches.Patch(color='b', label='60%')
	cyan = mpatches.Patch(color='c', label='40%')
	yellow = mpatches.Patch(color='y', label='20%')
	magenta = mpatches.Patch(color='m', label='Max')
	plt.legend(handles=[red,green,blue,cyan,yellow,magenta])
	#save plot
	plt.savefig("Reservoir "+title+" Rule Curve"+'.png',dpi=150)
	plt.close()
	
def twin_plot(data1,title1,data2,title2,years,reliability,resiliency,vulnerability):
	col_labels=['Reliability','Resiliency','Vulnerability']
	table_vals=[[round(reliability,4),round(resiliency,4),round(vulnerability,4)]]
	the_table = plt.table(cellText=table_vals,
					colWidths = [0.14]*3,
					colLabels=col_labels,
					colLoc='center',
					cellLoc='center',
					loc='upper left')
	#plot data
	months=[0]*int(years*12)
	for i in range(1,len(months)+1):
		months[i-1]=i
	plt.plot(months, data1, 'r')
	plt.plot(months, data2, 'b')
	#labels
	plt.xlabel("Time (Months)")
	plt.ylabel("Volume (MCM)")
	plt.title("Reservoir "+title1+" and "+title2)
	#axes limits
	axes = plt.gca()
	axes.set_xlim([1,len(months)])
	axes.set_ylim([0,max(max(data1),max(data2))*1.12])
	#legend
	red_patch = mpatches.Patch(color='r', label=title1)
	blue_patch = mpatches.Patch(color='b', label=title2)
	plt.legend(handles=[red_patch,blue_patch])
	#save plot
	plt.savefig("Reservoir "+title1+" and "+title2+'.png',dpi=150)
	plt.close()


def main():
	filename='results.txt'
	#read data from file
	(reliability,resiliency,vulnerability,demands,releases,inflows,storage)=read_results_file(filename)
	years=len(demands)/12
	#rule curves
	rule_curve(releases,"Release",reliability,resiliency,vulnerability)
	rule_curve(storage,"Storage",reliability,resiliency,vulnerability)
	#series plot
	twin_plot(demands,"Demands",releases,"Releases",years,reliability,resiliency,vulnerability)
	twin_plot(inflows,"Inflows",storage,"Storage",years,reliability,resiliency,vulnerability)

if __name__ == "__main__":
    main()

