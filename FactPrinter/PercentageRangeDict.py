def instantiate_percentage_dict():
	new_dict={
		(0,10):[],
		(10,20):[],
		(20, 30): [],
		(30, 40): [],
		(40, 50): [],
		(50, 60): [],
		(60, 70): [],
		(70, 80): [],
		(80, 90): [],
		(90, 101): []
	}
	return new_dict

def add_gp_to_perc_range_dict(perc_range_dict,gp,field_partition):

	if gp==0:
		return
	for ranges in perc_range_dict:
		begin=ranges[0]
		end=ranges[1]
		if begin<=gp<end:
				perc_range_dict[ranges].append((field_partition.encode('utf-8'),gp))
				break

