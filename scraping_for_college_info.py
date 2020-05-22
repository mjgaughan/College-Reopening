"""
author: Jake Gaughan

This program scrapes information about a given college or university from the National Center for Education Statistics website

The information grabbed is:
- student body size
- # of undergraduates on financial aid
- where students are from
- acceptance rate
- 25/75 percintiles of ACT scores

I used Mechanize and BeautifulSoup4 for this. And had the program return a list of informaiton on the school.
"""
import mechanize, bs4

#Mechanize housekeeping

#Browser
br = mechanize.Browser()
# Don't handle HTTP-EQUIV headers (HTTP headers embedded in HTML).
br.set_handle_equiv(False)
# Ignore robots.txt.  Do not do this without thought and consideration.
br.set_handle_robots(False)
# Don't add Referer (sic) header
br.set_handle_referer(False)
# Don't handle Refresh redirections
br.set_handle_refresh(False)


# Browser options
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_robots(False)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#searching and scraping from National Center for Education Statistics
def  lookup(college):
    #college_name = 'University of Alabama'
    college_stats = []
    for info in college:
        college_stats.append(info)
    college_name = college[0]
    save = 0
    #going to the NCES search bar
    br.open("https://nces.ed.gov/collegenavigator/")
    br.select_form('aspnetForm')
    #searching for a given college
    br.form['ctl00$cphCollegeNavBody$ucSearchMain$txtName'] = college_name
    br.submit()

    #navigating to the specific college's info page based on the search results
    can_we_find_the_school = False
    for link in br.links():
        if link.text == college_name or link.text == "The " + college_name:
            request = br.click_link(link)
            response = br.follow_link(link)
            #print(response.geturl())
            can_we_find_the_school = True
            break

    #if you can't find a given school in the search results
    if can_we_find_the_school == False:
        print("we deadass can't find this school: " + college_name)
        return
    else:
        br.open(response.geturl())

    #opening up the page's links and tables
    for link in br.links():

        #I actually think there is a cleaner way to do this but it works this way and, quite frankly, I'm a little too afraid to change it
        if link.text == "Financial Aid":
            #open everything up and get ready to parse, using a mix of mechanize and BeautifulSoup4
            request = br.click_link(link)
            response = br.follow_link(link)
            source = br.open(response.geturl())
            soup = bs4.BeautifulSoup(source, 'lxml')

            #find all tables in the jawn
            table_rows = soup.find_all('tr')
            #go through all tables in the jawn, looking for specific information
            for tr in table_rows:
                #turn the HTML tables into something more readable
                td = tr.find_all('td')
                for j in td:
                    clean_td(j, college_stats)

                row = [i.text for i in td]
                #look for the 3 pieces of info we can get from the tables
                for i in row:
                    #save a given piece of information to the list
                    if save == 1:
                        college_stats.append(i)
                        save = 0
                    #this is for ACT scores, need to get both the 25% and the 75% numbers
                    if save == 2:
                        string = i
                        save += 1
                    elif save == 3:
                        string += "-" + i
                        college_stats.append(string)
                        save = 0
                    #flagging a piece of information for saving
                    if i == 'Campus setting:\xa0\xa0' or i == 'Student population:\xa0\xa0' or i == 'Grant or scholarship aid1' or i == 'Percent admitted':
                        save = 1
                    if i == 'ACT Composite':
                        save = 2
            break

    print("Done with " + college_name)
    #print(college_stats)
    return(college_stats)


#looking through image descriptions for more data (specifically for the ACT data)
def clean_td(tds, college_stats):
    td_data = []
    holding_string =""
    save_y_n = False
    td = str(tds)
    for i in td:
        if i == '"' and not save_y_n:
            save_y_n = True
        elif i == '"' and save_y_n:
            save_y_n = False
            #scraping data on the geographical types of students at a given school
            #an issue that may arise is this is based on 2 digit places...
            if holding_string[0:31] == 'Undergraduate Student Residence':
                #this is in-state
                college_stats.append(holding_string[43:47])
                #this is out-of-state
                college_stats.append(holding_string[62:66])
                #this is international
                college_stats.append(holding_string[86:89])

            holding_string = ""
        elif save_y_n:
            holding_string += i
