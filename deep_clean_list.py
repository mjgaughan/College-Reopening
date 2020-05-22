#cleaning from the Chronicle list
"""
author: Jake Gaughan

This file is for the cleaning of the Chronicle of Higher Education's data on college re-openings
The data can be found at https://www.chronicle.com/article/Here-s-a-List-of-Colleges-/248626?cid=wcontentgrid_hp_1b

I don't really feel like thoroughly commenting all of this one so I'll give a brief synopsis

- Most of the college names were fine so they're just added as is
- University systems
    - Some state university systems manifest themselves in weird ways
    - Cal States have their own case
    - So do UCs
    - Some other systems have their own case as their entry into NECS is formatted a certain way
    - Others follow a more uniform way of writing and those are grouped together too
    - Some others already have their names written in full, those are kept intact
- This file will grow as more failures and errors are found and optimized
"""

def deep_clean(clean_college_names):

    Cal_State = False
    U_Maine = False
    U_Nebraska = False
    U_Tennessee = False
    U_T = False
    U_Maryland = False
    intact_uni_system = False

    for college in clean_college_names:
        #print(college[0])
        clean_college = ""
        #University of Maryland system
        if U_Maryland:
            clean_college = college[0][2:]
            if clean_college == "University of Maryland, Eastern Shore":
                U_Maryland = False
                clean_college = "University of Maryland Eastern Shore"
            elif clean_college == "University of Maryland at College Park":
                clean_college = "University of Maryland-College Park"
            else:
                clean_college = "University of Maryland-Baltimore County"
            college[0] = clean_college
        #University of Texas System
        if U_T:
            clean_college = "University of Texas at " + college[0][college[0].index("—") + 2:]
            if college[0][college[0].index("—") + 2:]== "Tyler":
                U_T = False
            college[0] = clean_college
            #print(college[0])
            continue
        #University of Tennessee System
        if U_Tennessee:
            clean_college = "University of Tennessee" + "-" + college[0][2:]
            if college[0]== "— Martin":
                U_Tennessee = False
            college[0] = clean_college
            #print(college[0])
            continue
        #University of Nebraska System
        if U_Nebraska:
            if college[0][college[0].index("—") + 2:]== "Lincoln":
                clean_college = "Univeristy of Nebraska-Lincoln"
            else:
                clean_college = "University of Nebraska at " + college[0][college[0].index("—") + 2:]
            if college[0][college[0].index("—") + 2:]== "Omaha":
                U_Nebraska = False
            college[0] = clean_college
            #print(college[0])
            continue
        #University of Maine system
        if U_Maine:
            if college[0][college[0].index("Maine") + 9:]== "Machias":
                clean_college = "University of Maine at Machias"
            elif college[0]== "University of Maine — University of Southern Maine":
                U_Maine = False
                clean_college = college[0][college[0].index("—") + 2:]
            else:
                clean_college = "University of Maine at " + college[0][college[0].index("Maine") + 8:]
            college[0] = clean_college
            #print(college[0])
            continue
        #Cal States
        if Cal_State:
            #print("--------------")
            clean_college = "California State University" + "-" + college[0][college[0].index("—") + 2:]
            if "University" in college[0][college[0].index("—") + 2:]:
                clean_college = college[0][college[0].index("—") + 2:]
            #college[0] = clean_college
            if college[0]== "California State University — Stanislaus":
                Cal_State = False
            college[0] = clean_college
            #print(college[0])
            continue

        if intact_uni_system:
            #print(college[0][2:])
            clean_college = college[0][college[0].index("—") + 2:]
            if (clean_college == "Williston State College" or
                clean_college == "University of South Dakota" or
                clean_college == "Texas State University" or
                clean_college == "Valdosta State University" or
                clean_college == "University of New Orleans" or
                clean_college == "Weber State University"):
                intact_uni_system = False
                #print("check off")
            #clean_college = college[0][2:]
            #print("this should be a college")
            college[0] = clean_college
            #print(college[0])
            continue

        #23 CSU schools
        if "California State University — Bakersfield" == college[0]:
            clean_college = "California State University" + "-" + college[0][college[0].index("—") + 2:]
            college[0] = clean_college
            #print("Cal_State-----------------------")
            #print(college[0])
            Cal_State = True
            #how to denote to add them differently

        #everything else that is a system
        elif (college[0] == "North Dakota University system" or
                college[0]== "South Dakota Board of Regents" or
                college[0]== "Texas State University system" or
                college[0]== "University of Georgia system" or
                college[0]== "University of Louisiana system" or
                college[0]== "Utah System of Higher Education"):
            intact_uni_system = True
            #print("check")
            #clean_college_names.remove(college)

        elif college[0]== "University of Maine system":
            U_Maine = True

        elif college[0]== "University of Nebraska system":
            U_Nebraska = True

        elif college[0]== "University of Tennessee system":
            U_Tennessee = True

        elif college[0]== "University of Texas system":
            U_T = True

        elif college[0] == "University System of Maryland":
            U_Maryland = True

        #Weird formating for the UC system, needed to clean up
        elif "University of California" in college[0]:
            if college[0]== "University of California, Los Angeles":
                clean_college = "University of California-Los Angeles"
            else:
                clean_college = "University of California-" + college[0][28:]
            college[0] = clean_college


        #Somethings I had noticed!
        elif college[0]== "University of Colorado at Boulder":
            college[0] = ("University of Colorado Boulder")

        elif (college[0] == "University of Alabama system" or
                college[0]== "University of Arkansas System"):
                college[0] = (college[0][:-7])
                if college[0] == "University of Alabama":
                    college[0] = "The " + college[0]

        elif college[0] == "Arizona State University":
            college[0] = "Arizona State University-Tempe"

        elif college[0] == "University of Alaska, Anchorage":
            college[0] = "University of Alaska Anchorage"

        elif college[0][:24] == "University of Wisconsin":
                college[0] = "University of Wisconsin-" + college[0][college[0].index("at") + 3:]

        elif "College" in college[0]or "University" in college[0]:
            college[0] = college[0]

        else:
            clean_college_names.remove(college)
        #print(college[0])
    #print(clean_college_names)
    return clean_college_names
