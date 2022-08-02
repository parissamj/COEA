#LNG_project_sensitivity
from map_to_drive import map_to_drive
import pandas as pd
import openpyxl

def colnum_string(n):
    #covnverts number n to the column string - ie C = 3, AB = 28
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def open_sensitivity_doc():
	#open with pandas
	#csv_location = "LNG_OPGEE_Sensitivity.csv"
	csv_location = "C:/Users/Parissa/Documents/Theme 2/Tight Gas Project/Parissa/OPGEE Runs/V3.0/Sensitivity/Sensitivity Updated/LNG_OPGEE_Sensitivity_Updated_WCSB.csv"

	df = pd.read_csv(csv_location)

	#print(list(df))

	#print(df["Input Row Number"])

	return df


def sensitivity_to_OPGEE():

	#this will take the base case inputs and vary them by a percentage 
	#for a simple sensitivity analysis 

	df = open_sensitivity_doc()
	df = df.dropna(axis=0, how='all')

	#TO GET A LIST OF ALL FIELDS FOR SENSITIVITY ANALYSIS
	field_list = []
	for field in list(df):
		if ('Low' not in field) and ('High' not in field) : field_list.append(field)
	

	#SET A SPECIFIC SET OF FIELDS HERE!
	field_list = ['Duvernay']

	print('FIELDS BEING ASSESSED')
	for field in field_list: print(field)
	print('\n')
	
	for field in field_list:

		#this needs to be a V2 edit suitable for all fields....

		csv_name = "OPGEE_v2.0_LNG_Edit.xlsm"
		#path = map_to_drive() + "C:/Users/Parissa/Documents/Theme 2/Tight Gas Project/Parissa/OPGEE Runs/V3.0/Sensitivity/" + csv_name
		path = r"C:/Users/Parissa/Documents/Theme 2/Tight Gas Project/Parissa/OPGEE Runs/V3.0/Sensitivity/" + csv_name
		wb=openpyxl.load_workbook(filename = path, read_only=False, keep_vba=True)
		sheetlist = wb.sheetnames

		#-----------OPGEE_input Sheet data ----------------
		for sheet in sheetlist:
			if sheet == 'Inputs':
				inputs_sheet = wb[sheet]

		#uncomment for mulltiple sheets
		initial_column_number = 8
		column_number = initial_column_number # (A = 0) 8 equates to I using colnum_string - this is where we start out input data

		min_max = ['Low - ','High - ']

		print('\n')
		print(field)

		for low_high in min_max:
			#Iterate through low and high
			for i, row in enumerate(df["Input Row Number"].values):
				#iterate through the input row numbers for OPGEE
				change = df["Change"].values[i] #0 or 1
				input_name = df['Input Name'].values[i] #input name
				position = str(colnum_string(column_number)) + str(int(row))
				#print(position)
				input_value = df[field].values[i]
				#inputs_sheet[position] = str(input_value)
				if change == 1:
					#print('\n')
					#print(position)
					for j, row_2 in enumerate(df["Input Row Number"].values):
						print "j="+ str(j) + " row_2=" + str(row_2) + "\n"
						position = str(colnum_string(column_number)) + str(int(row_2)) #position of input
						#print(position)
						if (row_2 == row and change == 1):
							input_value = df[low_high + field].values[j]
							try: inputs_sheet[position] = float(input_value)
							except: inputs_sheet[position] = str(input_value)			
						else:
							input_value = df[field].values[j]
							try: inputs_sheet[position] = float(input_value)
							except: inputs_sheet[position] = str(input_value)
						if input_name in ['N2','CO2','C2','C3','C4+','H2S']:
							#we are changing gas composition and therefore have to change C1 accordingle
							val_change = float(df[low_high + field].values[i]) - float(df[field].values[i])
							c1_dflocation = list(df["Input Name"].values).index('C1')
							c1_input_location = int(df["Input Row Number"].values[c1_dflocation])
							c1_base = float(df[field].values[c1_dflocation])
							c1_new =  c1_base - val_change
							inputs_sheet[str(colnum_string(column_number)) + str(c1_input_location)] = c1_new 
							

						#inputs_sheet[position] = str(input_value)

					inputs_sheet[str(colnum_string(column_number)) + str(153)] = low_high + ' ' + str(input_name)
					print(low_high, df["Input Name"].values[i])
					column_number = column_number + 1
			
			print('\n')
					#break
				

		#we use the project name we specify at the start
		export_file_name = csv_name + '_' + "Sens_"+ field + ".xlsm"
		#export_file_name = csv_name + '_All_Fields' + ".xlsm"

		#file_save_location = map_to_drive() + "C:/Users/Parissa/Documents/Theme 2/Tight Gas Project/Parissa/OPGEE Runs/V3.0/Sensitivity/Sensitivity Updated/OPGEE" + export_file_name
		file_save_location = "C:/Users/Parissa/Documents/Theme 2/Tight Gas Project/Parissa/OPGEE Runs/V3.0/Sensitivity/Sensitivity Updated/OPGEE" + export_file_name
		wb.save(file_save_location)

		wb.close()
		#break

if __name__ == '__main__':

	sensitivity_to_OPGEE()