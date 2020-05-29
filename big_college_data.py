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
    with open('Chronicle_3.csv') as csv_file:
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
                    """
                    if row[-1] != "":
                        plans = row[-1]
                    elif row[4] != "":
                        plans = row[4]
                    else:
                    """
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
    with open('new_queries.csv' , 'w' , newline = '') as file:
        writer = csv.writer(file)
        #top row
        writer.writerow(["School Name", "Control", "State", "Plan", "Setting","Size", "UG_FinAid", "In-State", "OState", "Int.", "Acceptance Rate", "25/75 ACT"])
        #for each college, lookup data for it and write it into the csv
        for college in clean_college_names:
            holding = lookup(college)
            #if there is a response from the query
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

#function for updating the csv's with new information from the Chronicle's website
def updating_info(clean_college_names):
    existing_data = []
    leftovers = []
    #reading from the existing data and writing it to a list
    with open('existing_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            existing_data.append(row)
    #going through the new data and checking if the school already exists in the old one
    for college in clean_college_names:
        is_it_in = False
        for college_1 in existing_data:
            #if it already exists
            if college[0] == college_1[0]:
                is_it_in = True
                break
        #if so, replace the old plan with the new one
        if is_it_in:
            college_1[3] = college[3]
        #if not, stash it in this other list
        else:
            leftovers.append(college)
    #make a new csv with all of the updated data
    with open('fresh_data.csv' , 'w' , newline = '') as file:
        writer = csv.writer(file)
        #top row
        writer.writerow(["School Name", "Control", "State", "Plan", "Setting","Size", "UG_FinAid", "In-State", "OState", "Int.", "Acceptance Rate", "25/75 ACT"])
        for school in existing_data:
            writer.writerow(school)
    #for all of the schools that are new to the project
    writing_into_csv(leftovers)



if __name__ == "__main__":
    #grabbing names
    institution_names()
    #cleaning them
    clean_college_names = deep_clean(dirty_college_names)
    #searching them
    #print(clean_college_names)
    updating_info(clean_college_names)
    #writing_into_csv(clean_college_names)
