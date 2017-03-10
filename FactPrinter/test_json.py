import json
import math
from pprint import pprint
from QuartileCalculation import *
from PercentageRangeDict import *
from testdata import *

#-------------------------------------------------------------------------------------------
data = u'data'
perc = u'perc'
partition_field = u'partition_field'
values_lg = u'value_global_local'
global_perc=u'global_perc'
local_perc=u'local_perc'
#-------------------------------------------------------------------------------------------

def separator():
	print "-------------------------------------------------------------------------"

def precedent_generator(value,quartile1,quartile3):
	if value>quartile3:
		return "Amazingly, a whopping "
	elif value<quartile1:
		return "Only "
	else:
		return "About "
def get_average_percentage(l):
	return reduce(lambda x, y: x + y, l) / len(l)

def global_perc_trend_statistics(perc_range_dict,field1,field2,trend_ratio,partition_field):
	for ranges in perc_range_dict:
		list_of_fields_gps=perc_range_dict[ranges]
		if list_of_fields_gps:
			value_gp_list=[]
			state_list=[]
			for tup in list_of_fields_gps:
				state_list.append(tup[0])
				value_gp_list.append(tup[1])
			avg_percentage=get_average_percentage(value_gp_list)

			print "Approximately "+str(avg_percentage)+"% villages in the states of "+str(state_list)+" have the " \
			"ratio between "+field1+" and "+field2+" as "+str(trend_ratio)

def global_perc_based_trend_generator(data_dict,field1,field2,partition_field,total_no_trends):
	#Q : Which states / How many states have x% of their villages following the ratio trend ?
	for trend_no in range(0,total_no_trends):
		#print trend_no
		trend_ratio = float(data_dict[trend_no][data][2])
		perc_range_dict=instantiate_percentage_dict()
		for field_partition in data_dict[trend_no][values_lg]:
			gp=(data_dict[trend_no][values_lg][field_partition][global_perc])*100
			#print gp
			add_gp_to_perc_range_dict(perc_range_dict,gp,field_partition)
		#print perc_range_dict
		global_perc_trend_statistics(perc_range_dict,field1,field2,trend_ratio,partition_field)


#This tells us how much percentage of the villages follow the trends(equivalent to ratio)
def basic_perc_based_trend_generate(data_dict,field1,field2,total_no_trends):
	perc_list=[]
	trend_perc_dict=dict()
	for trend_no in range(0,total_no_trends):
		percentage=float(data_dict[trend_no][perc])
		perc_list.append(percentage)
		trend_perc_dict[trend_no]=percentage
	perc_list.sort()

	q1 = quartiles(perc_list)[0]
	q3 = quartiles(perc_list)[1]

	for trend_no in range(0,len(data_dict)):
		trend_ratio=float(data_dict[trend_no][data][2])
		print (precedent_generator(trend_perc_dict[trend_no], q1, q3) + str(
				round(trend_perc_dict[trend_no], 4)) + "% villages have "+field1
				   + " = "+str(data_dict[trend_no][data][0][1])+" and "+ field2 +" = "+str(data_dict[trend_no][data][1][1]) +".")
		#Print Ratio instead of numbers
		"""
		print (precedent_generator(trend_perc_dict[trend_no],q1,q3) + str(round(trend_perc_dict[trend_no],4)) + "% villages have a ratio of " + str(
			trend_ratio) + " between " + field1
			   + " and " + field2 + ".")
		"""


# Tells us which factor prevails in the trends
def compare_factors_based_trend_generate(data_dict,field1,field2,total_no_trends):
	factor1 = 0
	factor2 = 0
	equality_factor = 0
	for trend_no in range(0,total_no_trends):
		trend_ratio=data_dict[trend_no][data][2]
		if trend_ratio>1:
			factor1+=1
		elif trend_ratio==1:
			equality_factor+=1
		else:
			factor2+=1

	factor1=str(factor1)
	factor2=str(factor2)
	equality_factor=str(equality_factor)
	print "Out of "+str(total_no_trends)+" trends, "+field1+" dominates "+field2+" "+factor1+" times!"
	print "Out of " + str(total_no_trends) + " trends, " + field2 + " dominates " + field1 + " " + factor2 + " times!"
	print "Out of "+str(total_no_trends)+" trends, "+field1+" and "+field2+" were equal "+equality_factor+" number of times"

def ratio_partition_based_trend_generator(data_dict, field1, field2, partition, total_no_trends):
	#how to partition when the end point is not known ?
	#what can we gain by knowing which trends have similar ratios ?
	pass

def run_test():

	with open('C:\Users\deb\Desktop\FYP\Resources\Facts_data-MaleFemale.json') as data_file:
		data_dict = json.load(data_file)
	#pprint(data_dict)

	sample_data_content=data_dict[0]
	field1,field2=sample_data_content[data][0][0].encode('utf-8'),sample_data_content[data][1][0].encode('utf-8')
	partition=sample_data_content[partition_field].encode('utf-8')
	total_no_trends=len(data_dict)

	"""
	print "Total number of trends generated based on Ratio between "+field1+" and "+field2+" are : "+str(total_no_trends)
	separator()
	compare_factors_based_trend_generate(data_dict, field1, field2, total_no_trends)
	separator()
	basic_perc_based_trend_generate(data_dict,field1,field2,total_no_trends)
	separator()

	"""
	global_perc_based_trend_generator(data_dict,field1,field2,partition,total_no_trends)
	separator()


run_test()


