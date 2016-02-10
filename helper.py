#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	try: 
		for attribute, value in dictIn.items():
			print('{} : {}'.format(attribute, value))
		print('\n')
	except:
		f1.write('\n =============================== \n PRINTING ISSUE FOR UNICODE \n =============================== \n')
