from scipy.stats.stats import pearsonr   
from random import randint
import random

def calc_correlation (list1,list2):
	print pearsonr(list1,list2)


def getNewList(start,end,passedlist):
	templist=[]
	mapping=dict()
	random_list = range(start, end)
	for i in range(0,len(passedlist)):
		if passedlist[i] in mapping:
			templist.append(mapping[passedlist[i]])
		else:
			mapping[passedlist[i]]=random_list[i]
			templist.append(mapping[passedlist[i]])

	print "temporary list created is :"+str(templist)
	print mapping
	return templist
	
def calculate_list(list1,list2,list1Flag,list2Flag):
	lenlist1=len(list1)
	if list1Flag and list2Flag:
		print "Both are string lists"
		list1=getNewList(1,lenlist1,list1)
		list2=getNewList(1,lenlist1,list2)
		calc_correlation(list1,list2)
	elif list1Flag:
		list2=map(int, list2)
		print "1 is a string list"
		list1=getNewList(1,lenlist1,list1)
		calc_correlation(list1,list2)
	elif list2Flag:
		list1=map(int, list1)
		print "2 is a string list"
		list2=getNewList(1,lenlist1,list2)
		calc_correlation(list1,list2)
	else:
		list1=map(int, list1)
		list2=map(int, list2)
		print "both are number list"
		calc_correlation(list1,list2)


def main():
	list1 = raw_input().split() 
	list2 = raw_input().split()

	try:
		int(list1[0])
	except ValueError:
		list1Flag = True
	else:
		list1Flag= False # not a string
	try:
		int(list2[0])
	except ValueError:
		list2Flag = True
	else:
		list2Flag= False
 
	#Assumption : both lists are same length ; else correlation cant be calculated
	if len(list1)!=len(list2):
		print "length of both lists need to match! Try again"
	else:
		calculate_list(list1,list2,list1Flag,list2Flag)
main()
