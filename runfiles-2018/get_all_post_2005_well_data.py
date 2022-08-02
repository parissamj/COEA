#returns all post 2005 well data
import os
import csv
import collections
import time
from datetime import datetime
import re
from map_to_drive import map_to_drive #path to Project Data folder



def get_all_post_2005_well_data(GAS_ONLY = True):

    #print('\nGETTING ALL POST 2005 WELL DATA')
    print('\nThis function is getting ALL gas producing wells with GOR > 10000scf/bbl')
    print('The database was exported from geoSCOUT on 25-Feb-2019\n')

    project_name = str(raw_input('Firstly, what would you like to name the Project?   '))
    print('\n')

    well_data = collections.OrderedDict()
    well_data_headings = []

    wells_list = []
    array = []
    #file_location = map_to_drive() + "/Project Data/geoSCOUT_data/weyburn-estevan.csv"
    #file_location = map_to_drive() + "Project Data/geoSCOUT_data/Canadian_LNG_well_data.csv"
    file_location = map_to_drive() + "Project Data/geoSCOUT_data/Post 2005 well_data.csv"


    #Searching for wells
    print('\nSearching For Wells...\n')
    timer = time.time()


    with open(file_location) as f:
        reader = csv.reader(f)
        for row in reader:
           
            if row[0] == 'Sort Format Well ID (Long)':
                well_data_headings = row
                f_12_gas_index = row.index('First 12 mo. Total GAS (e3m3)')
                f_12_oil_index = row.index('First 12 mo. Total OIL (m3)')
                f_12_cnd_index = row.index('First 12 mo. Total CND (m3)')
                GOR_index = row.index('First 12 mo. Ave GOR (m3/m3)')
                date_index = row.index('Date Drlg Completed')

            if row[0] != 'Sort Format Well ID (Long)':
                year = row[date_index][-4:]
                #print year
                wellid = row[well_data_headings.index('CPA Well ID')]
               
                if not GAS_ONLY:
                    if wellid not in well_data:
                        wells_list.append(wellid)
                        well_data[wellid] = row

                if GAS_ONLY:
                    if row[f_12_gas_index] == '':
                        #no production history, we pass this well
                        continue

                    else:
                        #get first 12 month production
                        f_12_gas = float(row[f_12_gas_index])
                        f_12_oil = float(row[f_12_oil_index])
                        f_12_cnd = float(row[f_12_cnd_index])

                        if (f_12_cnd + f_12_oil) == 0 and f_12_gas > 0:
                            #no liquids production and only gas production
                            if wellid not in well_data:
                                wells_list.append(wellid)
                                well_data[wellid] = row

                        elif (f_12_cnd + f_12_oil) > 0:
                            #we have liquid production, check GOR is above 10,000 scf/bbl (1781 m3/m3)
                            GOR = f_12_gas*1000/(f_12_cnd + f_12_oil)
                            if GOR > 1781:
                                if wellid not in well_data:
                                    wells_list.append(wellid)
                                    well_data[wellid] = row


    print('Computational Time (s): ' + "%.4f" %(time.time() - timer) + '\n')

    print(str(len(wells_list)) + ' Wells Found Meeting Criteria\n')

    return well_data_headings, well_data, project_name


def get_tight_oil_wells():

    from emissions_sensitivity import get_all_emission_data

    print('\nGETTING TIGHT OIL DATA - ONLY WELLS PROD > 0.1 bbl/day\n')

    well_data = collections.OrderedDict()
    well_data_headings = []

    wells_list = []
    file_location = map_to_drive() + "/Project Data/geoSCOUT_data/Post 2005 Well Data.csv"

    #Searching for wells
    formation = str(raw_input('Enter the tight oil formation of interest or type all;   '))
    print('\nSearching For Wells...\n')
    timer = time.time()

    emissions_headings, tight_oil_wells = get_all_emission_data()

    with open(file_location) as f:
        reader = csv.reader(f)
        for row in reader:
           
            if row[0] == 'Sort Format Well ID (Long)':
                well_data_headings = row
                date_index = row.index('Date Drlg Completed')

            if row[0] != 'Sort Format Well ID (Long)':
               
                year = row[date_index][-4:]
                #print year
                wellid = row[well_data_headings.index('CPA Well ID')]
                if wellid in tight_oil_wells:
                    if formation.upper() == 'ALL':
                        #if year in ['2017']:
                        well_data[wellid] = row
                    elif formation == tight_oil_wells[wellid][emissions_headings.index('Formation')]:
                        #if year in ['2017']:
                        well_data[wellid] = row
               


    print('Computational Time (s): ' + "%.4f" %(time.time() - timer) + '\n')

    print(str(len(well_data)) + ' Wells Found Meeting Criteria\n')

    time.sleep(5)

    return well_data_headings, well_data

if __name__ == '__main__':
   
    well_data_headings, well_data  = get_all_post_2005_well_data()

    #well_data_headings, well_data  = get_tight_oil_wells()


