"""
author: Jake Gaughan, @falsejenga on Twitter/@mjgaughan on Github

This is the main file for the project, with the other files serving to hold specific functions
From this file we:
    - grab information and college names from the Chronicle of Higher Education's database
    - clean the entries into searchable names using deep_clean_list.py
    - Take information from the Chronicle's website using scraping_for_college_info.py
    - write to a new csv all of the informaiton gleaned
"""
import csv
from scraping_for_college_info import *
from deep_clean_list import *


#list of colleges
dirty_college_names = []
clean_college_names = []

#grabbing from the Chronicle list, self explanatory
def institution_names():
    global college_names
    #opening up the csv from the Chronicle
    with open('Chronicle_2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
            #print(f'{row[0]}')
                college_name = row[0]
                if college_name != "" and len(row) >= 4:
                    #private/public
                    private_public = row[1]
                    #state
                    state = row[2]
                    #grabbing the plans
                    if row[-1] != "":
                        plans = row[-1]
                    elif row[4] != "":
                        plans = row[4]
                    else:
                        plans = row[3]
                    #putting all of the info from the Chronicle into a packet
                    college_admissions_packet = [college_name, private_public, state, plans]
                    #add to the list of all colleges
                    dirty_college_names.append(college_admissions_packet)
            line_count += 1

#writing the info from the colleges into a csv file
def writing_into_csv(clean_college_names):
    trouble_shooting_misses = 0
    trouble_shooting_makes = 0
    #opening the csv
    with open('clean_info.csv' , 'w' , newline = '') as file:
        writer = csv.writer(file)
        #top row
        writer.writerow(["School Name", "Control", "State", "Plan", "Setting","Size", "UG_FinAid", "In-State", "OState", "Int.", "Acceptance Rate", "25/75 ACT"])
        #for each college, lookup data for it and write it into the csv
        for college in clean_college_names[164:]:
            holding = lookup(college)
            if holding != None:
                writer.writerow(holding)
                trouble_shooting_makes += 1
            else:
                trouble_shooting_misses += 1
            print(str(100 * (trouble_shooting_makes + trouble_shooting_misses) / len(clean_college_names)) + "% done")

        #for trouble shooting the accurace of the scraping
        print("----------------------------------------------")
        print("Missses: " + str(trouble_shooting_misses))
        print("Makes: " + str(trouble_shooting_makes))
        print("Accuracy: " + str(trouble_shooting_makes / (trouble_shooting_makes + trouble_shooting_misses)))
        print("----------------------------------------------")

if __name__ == "__main__":
    institution_names()
    clean_college_names = deep_clean(dirty_college_names)

    writing_into_csv(clean_college_names)
