from scipy.stats.stats import pearsonr   
from random import randint

def calc_correlation (list1,list2):
	print pearsonr(list1,list2)

def getRandomList(minR,maxR):
	templist=[]
	for i in range(0,maxR):
		templist.append(randint(minR,maxR))
	print "Temporary list generated : "+str(templist)
	return templist

def check_typeof_list(list1,list2):
	#assume that if the first element is a string, the rest are strings too 
	#This is inline with the clarification that mixed lists are not possible
	
	list1Flag=False
	list2Flag=False
	lenlist1=len(list1)
	if isinstance(list1[0], (str, unicode)):
		list1Flag=True
	if isinstance(list2[0], (str, unicode)):
		list2Flag=True

	if list1Flag and list2Flag:
		print "Both are string lists"
		list1=getRandomList(1,lenlist1)
		list2=getRandomList(1,lenlist1)
		calc_correlation(list1,list2)
	elif list1Flag:
		print "1 is a string list"
		list1=getRandomList(1,lenlist1)
		calc_correlation(list1,list2)
	elif list2Flag:
		print "2 is a string list"
		list2=getRandomList(1,lenlist1)
		calc_correlation(list1,list2)
	else:
		print "both are number list"
		calc_correlation(list1,list2)


def main():
	list1 = raw_input().split() 
	list2 = raw_input().split()
	#Assumption : both lists are same length ; else correlation cant be calculated
	if len(list1)!=len(list2):
		print "length of both lists need to match! Try again"
	else:
		check_typeof_list(list1,list2)
main()
