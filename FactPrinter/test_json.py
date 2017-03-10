import json
import math
from pprint import pprint
from QuartileCalculation import *
data_dict=[{u'data': [[u'Tot_Fem_Pop_of_Vil', 2], [u'Tot_Mal_Pop_of_Vil', 1], 2],
			  u'partition_field': u'Stat_Nam',
  			  u'perc': 0.6,
			  u'value_global_local':{
                          u'Karnataka': {u'global_perc': 0.6,
                                         u'local_perc': 0.5},
                          u'ANDHRA PRADESH': {u'global_perc': 0.66,
                                              u'local_perc': 0.33},
				  		  u'Andaman and Nicobar': {u'global_perc': 0.5,
									  				u'local_perc': 0.167}
			  						}

			  },
			{u'data': [[u'Tot_Fem_Pop_of_Vil', 1], [u'Tot_Mal_Pop_of_Vil', 1], 1],
						  u'partition_field': u'Stat_Nam',
						  u'perc': 0.3,
						  u'value_global_local':{
									  u'Karnataka': {u'global_perc': 0.4,
													 u'local_perc': 0.66},
									  u'ANDHRA PRADESH': {u'global_perc': 0.33,
														  u'local_perc': 0.33},
									  u'Andaman and Nicobar': {u'global_perc': 0.0,
																u'local_perc': 0.0}
												}

						  },
			 {u'data': [[u'Tot_Fem_Pop_of_Vil', 4], [u'Tot_Mal_Pop_of_Vil', 4], 1],
			  u'partition_field': u'Stat_Nam',
			  u'perc': 0.1,
			  u'value_global_local': {
				  u'Karnataka': {u'global_perc': 0.0,
								 u'local_perc': 0.0},
				  u'ANDHRA PRADESH': {u'global_perc': 0.0,
									  u'local_perc': 0.0},
				  u'Andaman and Nicobar': {u'global_perc': 0.5,
										   u'local_perc': 1.0}}
			  }
			 ]
#-------------------------------------------------------------------------------------------
data = u'data'
perc = u'perc'
partition_field = u'partition_field'
values_lg = u'value_global_local'
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
		print (precedent_generator(trend_perc_dict[trend_no],q1,q3) + str(round(trend_perc_dict[trend_no],4)) + "% villages have a ratio of " + str(
			trend_ratio) + " between " + field1
			   + " and " + field2 + ".")


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
	print "Out of "+str(total_no_trends)+" trends, "+field1+" is more than "+field2+" "+factor1+" times!"
	print "Out of " + str(total_no_trends) + " trends, " + field2 + " is less than " + field1 + " " + factor2 + " times!"
	print "Out of "+str(total_no_trends)+" trends, "+field1+" and "+field2+" were equal "+equality_factor+" number of times"

def run_test():
	with open('C:\Users\deb\Desktop\FYP\Resources\Facts_data-MaleFemale.json') as data_file:
		data_dict = json.load(data_file)
	sample_data_content=data_dict[0]
	field1,field2=sample_data_content[data][0][0].encode('utf-8'),sample_data_content[data][1][0].encode('utf-8')
	total_no_trends=len(data_dict)
	print "Total number of trends generated based on Ratio between "+field1+" and "+field2+" are : "+str(total_no_trends)
	separator()
	compare_factors_based_trend_generate(data_dict, field1, field2, total_no_trends)
	separator()
	basic_perc_based_trend_generate(data_dict,field1,field2,total_no_trends)
	separator()


run_test()


