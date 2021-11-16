#Web Browser Forensics Tool Prototype 1.0 - 40406078
import sqlite3
import os
import re
import json
import itertools
from itertools import chain
from operator import itemgetter

#How to run:
#Import required libraries
#Press run and follow output instructions and queries
#If a path file error occurs, input your own


def main():
    artifact1 = browser_selector()
    print('\n[+] - Would you like to check this artifact for emails? - [yes] or [exit]\n')
    email_input = input()
    if email_input == 'yes':
        emails(artifact1)
    else:
        pass
    print('\n[+] - Would you like to search this artifact for a specific keyword? - [yes] or [exit]\n')
    keyword_user_input = input()
    if keyword_user_input == "yes":
        keyword(artifact1)
    else:
        pass
    print("\n[+] - Would you like to analyse/select any more browsers simultaneously? - [yes] or [exit]\n")
    user_input = input()
    if user_input == "yes":
        artifact2 = browser_selector()
        artifact3 = artifact_merger(artifact1, artifact2)
        print('\n[+] - Would you like to check these artifacts for emails? - [yes] or [exit]\n')
        email_input2 = input()
        if email_input2 == 'yes':
            emails(artifact3)
        else:
            pass
        print('\n[+] - Would you like to search these artifacts for a specific keyword? - [yes] or [exit]\n')
        keyword_user_input2 = input()
        if keyword_user_input2 == "yes":
            keyword(artifact3)
        else:
            pass
        print('\n[+] - Would you like to select a third artifact to merge data with? - [yes] or [exit]\n')
        user_input2 = input()
        if user_input2 == "yes":
            artifact4 = browser_selector()
            artifact_merger2(artifact3, artifact4)
            print('\n[+] - Would you like to select a fourth artifact to merge data with? - [yes] or [exit]\n')
            user_input3 = input()
            if user_input3 == "yes":
                artifact5 = browser_selector()
                artifact6 = artifact_merger3(artifact4, artifact5)
                print('\n[+] - Would you like to check these artifacts for emails? - [yes] or [exit]\n')
                email_input3 = input()
                if email_input3 == 'yes':
                    emails(artifact6)
                else:
                    pass
                print('\n[+] - Would you like to search these artifacts for a specific keyword? - [yes] or [exit]\n')
                keyword_user_input3 = input()
                if keyword_user_input3 == "yes":
                    keyword(artifact6)
                else:
                    pass
    else:
        pass


def artifact_merger(a_1, a_2):
    merged_data = []
    artifact_1 = a_1
    artifact_2 = a_2
    for item in itertools.chain(artifact_1, artifact_2):
        merged_data.append(item)
    sorted_data = sorted(merged_data, key=itemgetter(1))  # sorting based on item [1]

    with open('duo_merged_data.js', 'w') as f:  # w to write over stuff, a to append/add to what's already there
        for row in sorted_data:
            f.write('\n')
            json.dump(row, f)
    f.close()
    print('\nA duo_merged_data.js file has been created with data from the *two* browser artifacts you selected!\n')
    return sorted_data

def artifact_merger2(a_1, a_2): #to keep the duo_merged_data file separate from triple_merged_data
    merged_data = []
    artifact_1 = a_1
    artifact_2 = a_2
    for item in itertools.chain(artifact_1, artifact_2):
        merged_data.append(item)
    sorted_data = sorted(merged_data, key=itemgetter(1))  # sorting based on item [1]

    with open('triple_merged_data.js', 'w') as f:  # w to write over stuff, a to append/add to what's already there
        for row in sorted_data:
            f.write('\n')
            json.dump(row, f)
    f.close()
    print('\nA triple_merged_data.js file has been created with data from the *three* browser artifacts you selected!\n')

def artifact_merger3(a_1, a_2): #to keep the duo_merged_data file separate from triple and quad
    merged_data = []
    artifact_1 = a_1
    artifact_2 = a_2
    for item in itertools.chain(artifact_1, artifact_2):
        merged_data.append(item)
    sorted_data = sorted(merged_data, key=itemgetter(1))  # sorting based on item [1]

    with open('quad_merged_data.js', 'w') as f:  # w to write over stuff, a to append/add to what's already there
        for row in sorted_data:
            f.write('\n')
            json.dump(row, f)
    f.close()
    print('\nA quad_merged_data.js file has been created with data from the *four* browser artifacts you selected!\n')


def emails(data): #finding the most used emails
    email_list = []

    data_list = list(chain.from_iterable(data)) #regex to put all emails into a list
    for email in data_list:
        try:
            email_regex = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
            email_list.extend(email_regex.findall(email))
        except Exception:
            pass

    if len(email_list) == 0:
        print('\nThis artifact doesn\'t have any emails!\n')
        return
    else:
        pass

    #counter for the number of emails in the list
    email_counter = {x:email_list.count(x) for x in email_list}

    print("\n[+] - The most frequent emails used sorted by use count:\n")
    # Modified from shorturl.at/juw89
    # itemgetter grabs the 2nd item (0, (1)) from the dictionary
    sorted_dict = dict(sorted(email_counter.items(), key=itemgetter(1), reverse = True))
    for i in sorted_dict:
        print(i + ': ' + str(sorted_dict[i]))


def keyword(data):
    print('\n[+] - Input the keyword you\'d like to search for:\n')
    user_input = input()
    broad_expression = re.compile('(?i)'+user_input)
    strict_expression = re.compile(user_input)

    print('\n[+] - Would you like a strict/lazy search or a broad/greedy search? - [strict] or [broad]\n ')
    search_input = input()

    broad_res = []
    strict_res = []

    if search_input == 'broad':
        for i in data:      #looking for keyword in list
            results = list(broad_expression.findall(str(i)))
            if bool(results):
                broad_res.append(i)
        if not broad_res:
            print('\n[+] - ' +user_input+ ' isn\'t present in the artifact provided!\n')
        else:
            print('\n[+] ' +user_input+ ' is present in the artifact - Printing Broad Search Output: \n')
            #print(data[0]) printing the column names but when data is merged the column names go to the bottom so it retrieves wrong data
            for i in broad_res:
                print(i)
    elif search_input == 'strict':
        for j in data:      #looking for keyword in list
            results2 = list(strict_expression.findall(str(j)))
            if bool(results2):
                strict_res.append(j)
        if not strict_res:
            print('\n[+] - ' +user_input+ ' isn\'t present in the artifact provided!\n')
        else:
            print('\n[+] ' +user_input+ ' is present in the artifact - Printing Strict Search Output: \n')
            #print(data[0])
            for j in strict_res:
                print(j)
    else:
        pass



#Function in charge of asking user which browser they want to analyse
def browser_selector():
    while True:
        print('\n[+] - Which web browser would you like to analyse? \n[chrome, firefox, edge, opera]\n')
        browser_input = input()

        if browser_input == "chrome":
            return(chrome())
        elif browser_input == "firefox":
            return(firefox())
        elif browser_input == "edge":
            return(edge())
        elif browser_input == "opera":
            return(opera())
        else:
            print("[+] - Try again - Make sure you select one of the available options \n")


#Function in charge of retrieving google chrome artifacts
def chrome():
    user = os.getlogin()
    max_count = 3
    count = 0
    while True:    #keeps the function going even after a successful output in case the user wants to analyse another artifact, only if the function is presented with an "exit" it'll go back to main()
        print('\n[+] - Which web browser artifact would you like to analyse? \n[Cookies, History, Downloads, Logins, Keywords (search terms)..] - or \'exit\' \n')
        artifact_input = input()
        if artifact_input == 'exit':
            break
        else:
            pass
        if artifact_input == "cookies" or artifact_input == "Cookies":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Google\Chrome\User Data\Default\Cookies".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors = "ignore") #ignore utf-8 encoding errors from one of the database columns
                #Chrome's base time is 01/01/1601 00:00:00.
                # To calculate local time, Chrome time has to be converted to seconds by dividing by one-million,
                # and then the seconds differential between 01/01/1601 00:00:00 and 01/01/1970 00:00:00 must be subtracted

                cur.execute('SELECT datetime(creation_utc / 1e6 - 11644473600, "unixepoch") AS creation_timestamp,'
                            ' datetime(last_access_utc / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp,'
                            'is_secure, is_httponly, is_persistent, priority, samesite, host_key, name '
                            ' FROM cookies ORDER BY creation_utc')
                data = cur.fetchall()

                #inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0,'Browser: Chrome')

                chrome_cookies = [] #creating a list with the browser tag that can be returned for merging artifacts later
                chrome_cookies.append(column_name)
                for index, tuple in enumerate(data):
                    chrome_cookies.append(("Chrome", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6], tuple[7], tuple[8]))

                with open('chrome_cookies.js', 'w') as f: #w to write over stuff, a to append/add to what's already there
                    for row in chrome_cookies:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA chrome_cookies.js file has been created with [Browser, Cookie creation timestamp, Cookie Last Access Timestamp,is_secure, is_httponly, is_persistent, priority, samesite, Host Key, Cookie Name] ordered by Cookie Creation Timestamp\n')
                return(chrome_cookies)
            except Exception as err: #This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0               #count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count: #This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":     #If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(creation_utc / 1e6 - 11644473600, "unixepoch") AS creation_timestamp,'
                            ' datetime(last_access_utc / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp,'
                            'is_secure, is_httponly, is_persistent, priority, samesite, host_key, name '
                            ' FROM cookies ORDER BY creation_utc')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Chrome')

                        chrome_cookies = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        chrome_cookies.append(column_name)
                        for index, tuple in enumerate(data):
                            chrome_cookies.append(("Chrome", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                                   tuple[6], tuple[7], tuple[8]))

                        with open('chrome_cookies.js','w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in chrome_cookies:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print('\nA chrome_cookies.js file has been created with [Browser, Cookie creation timestamp, Cookie Last Access Timestamp,is_secure, is_httponly, is_persistent, priority, samesite, Host Key, Cookie Name] ordered by Cookie Creation Timestamp\n')
                        return(chrome_cookies)
                    except Exception as err:
                        print("[+] - " + str(err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "downloads" or artifact_input == "Downloads":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Google\Chrome\User Data\Default\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(start_time / 1e6 - 11644473600, "unixepoch") AS download_start_timestamp,'
                    'last_modified, received_bytes, total_bytes, state,'
                    'current_path, url, referrer FROM downloads LEFT JOIN downloads_url_chains '
                    'ON downloads.id = downloads_url_chains.id ORDER BY start_time')
                data = cur.fetchall()

                #inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Chrome')

                chrome_downloads = []  # creating a list with the browser tag that can be returned for merging artifacts later
                chrome_downloads.append(column_name)
                for index, tuple in enumerate(data):
                    chrome_downloads.append(("Chrome", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                                   tuple[6], tuple[7]))

                with open('chrome_downloads.js','w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in chrome_downloads:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print('\nA chrome_downloads.js file has been created with [Browser, Download Timestamp, Last Modified, Received Bytes, Total_bytes, State(0/1), Download File Path, Download URL, Referrer] ordered by Download Timestamp \n')
                return(chrome_downloads)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(start_time / 1e6 - 11644473600, "unixepoch") AS download_start_timestamp,'
                            'last_modified, received_bytes, total_bytes, state,'
                            'current_path, url, referrer FROM downloads LEFT JOIN downloads_url_chains '
                            'ON downloads.id = downloads_url_chains.id ORDER BY start_time')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Chrome')

                        chrome_downloads = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        chrome_downloads.append(column_name)
                        for index, tuple in enumerate(data):
                            chrome_downloads.append(
                                ("Chrome", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                 tuple[6], tuple[7]))

                        with open('chrome_downloads.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in chrome_downloads:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA chrome_downloads.js file has been created with [Browser, Download Timestamp, Last Modified, Received Bytes, Total_bytes, State(0/1), Download File Path, Download URL, Referrer] ordered by Download Timestamp \n')
                        return(chrome_downloads)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "history" or artifact_input == "History":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Google\Chrome\User Data\Default\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute('SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls '
                            'ORDER BY last_visit_timestamp')
                data = cur.fetchall()

                cur.execute('SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls '
                            'ORDER BY visit_count DESC LIMIT 50')
                visit_count_data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Chrome')

                print('The top 50 most visited sites:\n')
                print(column_name, '\n')
                for i in visit_count_data:
                    print(i)

                chrome_history = []  # creating a list with the browser tag that can be returned for merging artifacts later
                chrome_history.append(column_name)
                for index, tuple in enumerate(data):
                    chrome_history.append(("Chrome", tuple[0], tuple[1], tuple[2], tuple[3]))

                with open('chrome_history.js','w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in chrome_history:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print('\nA chrome_history.js file has been created with [Browser, Last Visit Timestamp, Visit Count, Url] ordered by Last Visit Timestamp. \n')
                return(chrome_history)
            except Exception as err:
                print("[+] - " + str(err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                        'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp,'
                        ' visit_count, url, title FROM urls ORDER BY last_visit_timestamp')
                        data = cur.fetchall()

                        cur.execute(
                        'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls ORDER BY visit_count DESC LIMIT 50')
                        visit_count_data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Chrome')

                        print('The top 50 most visited sites:\n')
                        print(column_name, '\n')
                        for i in visit_count_data:
                            print(i)

                        chrome_history = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        chrome_history.append(column_name)
                        for index, tuple in enumerate(data):
                            chrome_history.append(("Chrome", tuple[0], tuple[1], tuple[2], tuple[3]))

                        with open('chrome_history.js',
                                'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in chrome_history:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print('\nA chrome_history.js file has been created with [Browser, Last Visit Timestamp, Visit Count, Url] ordered by Last Visit Timestamp. \n')
                        return(chrome_history)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "logins" or artifact_input == "Logins":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Google\Chrome\User Data\Default\Login Data".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                    'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                    ' username_value, origin_url'
                    ' FROM logins ORDER BY login_date_created')
                data = cur.fetchall()

                cur.execute(
                    'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                    'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                    ' username_value, origin_url'
                    ' FROM logins ORDER BY times_used DESC LIMIT 50')
                times_used_count_data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Chrome')

                print('The top 50 most used logins:\n')
                print(column_name,'\n')
                for i in times_used_count_data:
                    print(i)

                chrome_logins = []  # creating a list with the browser tag that can be returned for merging artifacts later
                chrome_logins.append(column_name)
                for index, tuple in enumerate(data):
                    chrome_logins.append(("Chrome", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))
                #items with incorrect timestamps (1601 00:00:00 etc) are so because the values on the table are null/0
                with open('chrome_logins.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in chrome_logins:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print('\nA chrome_logins.js file has been created with [Browser, Download Timestamp, Download File Path, Download URL] ordered by Download Timestamp \n')
                return(chrome_logins)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                            'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                            ' username_value, origin_url'
                            ' FROM logins ORDER BY login_date_created')
                        data = cur.fetchall()

                        cur.execute(
                            'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                            'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                            ' username_value, origin_url'
                            ' FROM logins ORDER BY times_used DESC LIMIT 50')
                        times_used_count_data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Chrome')

                        print('The top 50 most used logins:\n')
                        print(column_name, '\n')
                        for i in times_used_count_data:
                            print(i)

                        chrome_logins = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        chrome_logins.append(column_name)
                        for index, tuple in enumerate(data):
                            chrome_logins.append(("Chrome", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))

                        with open('chrome_logins.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in chrome_logins:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print('\nA chrome_logins.js file has been created with [Browser, Download Timestamp, Download File Path, Download URL] ordered by Download Timestamp \n')
                        return(chrome_logins)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "keywords" or artifact_input == "Keywords":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Google\Chrome\User Data\Default\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp,'
                    'term AS searched_keywords, url FROM keyword_search_terms LEFT JOIN urls ON keyword_search_terms.url_id = urls.id')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Chrome')

                chrome_keywords = []  # creating a list with the browser tag that can be returned for merging artifacts later
                chrome_keywords.append(column_name)
                for index, tuple in enumerate(data):
                    chrome_keywords.append(("Chrome", tuple[0], tuple[1], tuple[2]))

                with open('chrome_keywords.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in chrome_keywords:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA chrome_keywords.js file has been created with [Keywords searched, urls]. \n')
                return(chrome_keywords)
            except Exception as err:
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute('SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp,'
                    'term AS searched_keywords, url FROM keyword_search_terms LEFT JOIN urls ON keyword_search_terms.url_id = urls.id')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Chrome')

                        chrome_keywords = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        chrome_keywords.append(column_name)
                        for index, tuple in enumerate(data):
                            chrome_keywords.append(("Chrome", tuple[0], tuple[1], tuple[2]))

                        with open('chrome_keywords.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in chrome_keywords:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA chrome_keywords.js file has been created with [Keywords searched, urls]. \n')
                        return(chrome_keywords)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1

#Function in charge of retrieving firefox artifacts
def firefox():
    user = os.getlogin()
    max_count = 3
    count = 0
    while True:
        print('\nWhich web browser artifact would you like to analyse? \n[Cookies, History, Downloads, Logins..] - or \'exit\' \n')
        artifact_input = input()

        if artifact_input == "cookies" or artifact_input == "Cookies":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles\w3f17vy6.default-release\cookies.sqlite".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                # To calculate local time, Firefox time has to be converted to seconds by dividing by one-million,
                cur.execute('SELECT datetime(creationTime / 1e6, "unixepoch") AS creation_timestamp,'
                            'datetime(lastAccessed / 1e6, "unixepoch") AS last_accessed_timestamp,'
                            'isSecure, isHttpOnly, sameSite, host, name, value'
                            ' FROM moz_cookies ORDER BY creation_timestamp')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Firefox')

                firefox_cookies = []  # creating a list with the browser tag that can be returned for merging artifacts later
                firefox_cookies.append(column_name)
                for index, tuple in enumerate(data):
                    firefox_cookies.append(("Firefox", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                                   tuple[6], tuple[7]))

                with open('firefox_cookies.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in firefox_cookies:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA firefox_cookies.js file has been created with [Browser, Creation Timestamp, Last Accessed Timestamp, '
                    'isSecure, isHttpOnly, sameSite, host, name, value] ordered by Cookie Creation Timestamp.\n')
                return(firefox_cookies)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(creationTime / 1e6, "unixepoch") AS creation_timestamp,'
                            'datetime(lastAccessed / 1e6, "unixepoch") AS last_accessed_timestamp,'
                            'isSecure, isHttpOnly, sameSite, host, name, value'
                            ' FROM moz_cookies ORDER BY creation_timestamp')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Firefox')

                        firefox_cookies = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        firefox_cookies.append(column_name)
                        for index, tuple in enumerate(data):
                            firefox_cookies.append(
                                ("Firefox", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                 tuple[6], tuple[7]))

                        with open('firefox_cookies.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in firefox_cookies:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print('\nA firefox_cookies.js file has been created with [Browser, Creation Timestamp, Last Accessed Timestamp, '
                              'isSecure, isHttpOnly, sameSite, host, name, value] ordered by Cookie Creation Timestamp\n')
                        return(firefox_cookies)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "history" or artifact_input == "History":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles\w3f17vy6.default-release\places.sqlite".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                # To calculate local time, Firefox time has to be converted to seconds by dividing by one-million,
                cur.execute('SELECT datetime(last_visit_date / 1e6, "unixepoch") AS last_visit_timestamp,'
                            'visit_count, url, title FROM moz_places ORDER BY last_visit_timestamp')
                data = cur.fetchall()

                cur.execute(
                    'SELECT datetime(last_visit_date / 1e6, "unixepoch") AS last_visit_timestamp,'
                    'visit_count, url, title FROM moz_places ORDER BY visit_count DESC LIMIT 50')
                visit_count_data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Firefox')

                print('The top 50 most visited sites:\n')
                print(column_name, '\n')
                for i in visit_count_data:
                    print(i)

                firefox_history = []  # creating a list with the browser tag that can be returned for merging artifacts later
                firefox_history.append(column_name)
                for index, tuple in enumerate(data):
                    firefox_history.append(("Firefox", tuple[0], tuple[1], tuple[2], tuple[3]))

                with open('firefox_history.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in firefox_history:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA firefox_history.js file has been created with [Browser, Last Visit Timestamp, Visit Count, url, title] ordered by last visit timestamp\n')
                return(firefox_history)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(last_visit_date / 1e6, "unixepoch") AS last_visit_timestamp,'
                            'visit_count, url, title FROM moz_places ORDER BY last_visit_timestamp')
                        data = cur.fetchall()

                        cur.execute(
                            'SELECT datetime(last_visit_date / 1e6, "unixepoch") AS last_visit_timestamp,'
                            'visit_count, url, title FROM moz_places ORDER BY visit_count DESC LIMIT 50')
                        visit_count_data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Firefox')

                        print('The top 50 most visited sites:\n')
                        print(column_name, '\n')
                        for i in visit_count_data:
                            print(i)

                        firefox_history = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        firefox_history.append(column_name)
                        for index, tuple in enumerate(data):
                            firefox_history.append(("Firefox", tuple[0], tuple[1], tuple[2], tuple[3]))

                        with open('firefox_history.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in firefox_history:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA firefox_history.js file has been created with [Browser, Last Visit Timestamp, Visit Count, url, title] ordered by last visit timestamp\n')
                        return(firefox_history)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "downloads" or artifact_input == "Downloads":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles\w3f17vy6.default-release\places.sqlite".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database column
                # To calculate local time, Firefox time has to be converted to seconds by dividing by one-million,
                cur.execute('SELECT datetime(dateAdded / 1e6, "unixepoch") AS date_added,'
                            'datetime(lastModified / 1e6, "unixepoch") AS date_last_modified, place_id, content, url '
                            'FROM moz_annos LEFT JOIN moz_places ON moz_annos.place_id=moz_places.id ORDER BY date_added')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Firefox')

                firefox_downloads = []  # creating a list with the browser tag that can be returned for merging artifacts later
                firefox_downloads.append(column_name)
                for index, tuple in enumerate(data):
                    firefox_downloads.append(("Firefox", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))

                with open('firefox_downloads.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in firefox_downloads:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA firefox_downloads.js file has been created with [Browser, Date_added, Date_last_modified, Place_id, Content, URL] ordered by Date_added\n')
                return (firefox_downloads)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute('SELECT datetime(dateAdded / 1e6, "unixepoch") AS date_added,'
                            'datetime(lastModified / 1e6, "unixepoch") AS date_last_modified, place_id, content, url '
                            'FROM moz_annos LEFT JOIN moz_places ON moz_annos.place_id=moz_places.id ORDER BY date_added')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Firefox')

                        firefox_downloads = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        firefox_downloads.append(column_name)
                        for index, tuple in enumerate(data):
                            firefox_downloads.append(("Firefox", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))

                        with open('firefox_downloads.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in firefox_downloads:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA firefox_downloads.js file has been created with [Browser, Date_added, Date_last_modified, Place_id, Content, URL] ordered by Date_added\n')
                        return (firefox_downloads)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "keywords" or artifact_input == "Keywords":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles\w3f17vy6.default-release\formhistory.sqlite".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                # Firefox's base time is 01/01/1652 00:00:00.
                # To calculate local time, Firefox time has to be converted to seconds by dividing by one-million,
                cur.execute('SELECT datetime(firstUsed / 1e6, "unixepoch") AS date_first_used,'
                            'datetime(lastUsed / 1e6, "unixepoch") AS date_last_used, fieldname, value '
                            'FROM moz_formhistory ORDER BY date_first_used')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Firefox')

                firefox_keywords = []  # creating a list with the browser tag that can be returned for merging artifacts later
                firefox_keywords.append(column_name)
                for index, tuple in enumerate(data):
                    firefox_keywords.append(("Firefox", tuple[0], tuple[1], tuple[2], tuple[3]))

                with open('firefox_keywords.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in firefox_keywords:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA firefox_keywords.js file has been created with [Browser, Date_added, Date_last_modified, Place_id, Content, URL] ordered by Date_added\n')
                return (firefox_keywords)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute('SELECT datetime(firstUsed / 1e6, "unixepoch") AS date_first_used,'
                                    'datetime(lastUsed / 1e6, "unixepoch") AS date_last_used, fieldname, value '
                                    'FROM moz_formhistory ORDER BY date_first_used')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Firefox')

                        firefox_keywords = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        firefox_keywords.append(column_name)
                        for index, tuple in enumerate(data):
                            firefox_keywords.append(("Firefox", tuple[0], tuple[1], tuple[2], tuple[3]))

                        with open('firefox_keywords.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in firefox_keywords:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA firefox_keywords.js file has been created with [Browser, Date_added, Date_last_modified, Place_id, Content, URL] ordered by Date_added\n')
                        return (firefox_keywords)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "logins" or artifact_input == "Logins": # parsing a json file instead
            try:
                with open(r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles\w3f17vy6.default-release\logins.json".format(user), 'r') as g:
                    data = json.load(g)
                g.close()
                firefox_logins = []
                with open('firefox_logins.js', 'w') as f:  # w to write over stuff, a to append/add to what's already there
                    dict_counter = 0
                    f.write('Logins:')
                    while dict_counter < len(data['logins']):   #while loop to dump the nested dictionary values info into the json file
                        f.write('\n')
                        json.dump((data['logins'][dict_counter]), f)
                        firefox_logins.append(data['logins'][dict_counter])
                        dict_counter += 1
                    else:
                        pass
                f.close()
                print(
                    '\nA firefox_logins.js file has been created with the relevant data from the login.json file.\n')
                return (firefox_logins)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()

                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        with open(url_input, 'r') as g:
                            data = json.load(g)
                        g.close()

                        firefox_logins = []
                        with open('firefox_logins.js','w') as f:  # w to write over stuff, a to append/add to what's already there
                            dict_counter = 0
                            f.write('Logins:')
                            while dict_counter < len(data['logins']):  # while loop to dump the nested dictionary values info into the json file
                                f.write('\n')
                                json.dump((data['logins'][dict_counter]), f)
                                firefox_logins.append(data['logins'][dict_counter])
                                dict_counter += 1
                            else:
                                pass
                        f.close()
                        print('\nA firefox_logins.js file has been created with [Browser, Date_added, Date_last_modified, Place_id, Content, URL] ordered by Date_added\n')
                        return (firefox_logins)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        else:
            break

#Function in charge of retrieving opera artifacts
def opera():
    user = os.getlogin()
    max_count = 3
    count = 0
    while True:  # keeps the function going even after a successful output in case the user wants to analyse another artifact, only if the function is presented with an "exit" it'll go back to main()
        print(
            '\nWhich web browser artifact would you like to analyse? \n[Cookies, History, Downloads, Logins, Keywords (search terms)..] - or \'exit\' \n')
        artifact_input = input()
        if artifact_input == 'exit':
            break
        else:
            pass
        if artifact_input == "cookies" or artifact_input == "Cookies":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Roaming\Opera Software\Opera Stable\Cookies".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                # Opera's base time is 01/01/1601 00:00:00.
                # To calculate local time, Opera time has to be converted to seconds by dividing by one-million,
                # and then the seconds differential between 01/01/1601 00:00:00 and 01/01/1970 00:00:00 must be subtracted

                cur.execute(
                    'SELECT datetime(creation_utc / 1e6 - 11644473600, "unixepoch") AS creation_timestamp,'
                    ' datetime(last_access_utc / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp,'
                    'is_secure, is_httponly, is_persistent, priority, samesite, host_key, name '
                    ' FROM cookies ORDER BY creation_utc')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Opera')

                opera_cookies = []  # creating a list with the browser tag that can be returned for merging artifacts later
                opera_cookies.append(column_name)
                for index, tuple in enumerate(data):
                    opera_cookies.append(("Opera", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                           tuple[6], tuple[7], tuple[8]))

                with open('opera_cookies.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in opera_cookies:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA opera_cookies.js file has been created with [Browser, Cookie creation timestamp, Cookie Last Access Timestamp,is_secure, is_httponly, is_persistent, priority, samesite, Host Key, Cookie Name] ordered by Cookie Creation Timestamp\n')
                return (opera_cookies)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        # Opera's base time is 01/01/1601 00:00:00.
                        # To calculate local time, Opera time has to be converted to seconds by dividing by one-million,
                        # and then the seconds differential between 01/01/1601 00:00:00 and 01/01/1970 00:00:00 must be subtracted

                        cur.execute(
                            'SELECT datetime(creation_utc / 1e6 - 11644473600, "unixepoch") AS creation_timestamp,'
                            ' datetime(last_access_utc / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp,'
                            'is_secure, is_httponly, is_persistent, priority, samesite, host_key, name '
                            ' FROM cookies ORDER BY creation_utc')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Opera')

                        opera_cookies = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        opera_cookies.append(column_name)
                        for index, tuple in enumerate(data):
                            opera_cookies.append(("Opera", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                                  tuple[6], tuple[7], tuple[8]))

                        with open('opera_cookies.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in opera_cookies:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA opera_cookies.js file has been created with [Browser, Cookie creation timestamp, Cookie Last Access Timestamp,is_secure, is_httponly, is_persistent, priority, samesite, Host Key, Cookie Name] ordered by Cookie Creation Timestamp\n')
                        return (opera_cookies)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "downloads" or artifact_input == "Downloads":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Roaming\Opera Software\Opera Stable\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(start_time / 1e6 - 11644473600, "unixepoch") AS download_start_timestamp,'
                    'datetime(last_access_time / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp, received_bytes, total_bytes, state,'
                    'current_path, url, referrer FROM downloads LEFT JOIN downloads_url_chains '
                    'ON downloads.id = downloads_url_chains.id ORDER BY start_time')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Opera')

                opera_downloads = []  # creating a list with the browser tag that can be returned for merging artifacts later
                opera_downloads.append(column_name)
                for index, tuple in enumerate(data):
                    opera_downloads.append(("Opera", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                             tuple[6], tuple[7]))
                with open('opera_downloads.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in opera_downloads:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA opera_downloads.js file has been created with [Browser, Download Timestamp, Last Accessed Timestamp, Received Bytes, Total_bytes, State(0/1), Download File Path, Download URL, Referrer] ordered by Download Timestamp \n')
                return (opera_downloads)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(start_time / 1e6 - 11644473600, "unixepoch") AS download_start_timestamp,'
                            'datetime(last_access_time / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp, received_bytes, total_bytes, state,'
                            'current_path, url, referrer FROM downloads LEFT JOIN downloads_url_chains '
                            'ON downloads.id = downloads_url_chains.id ORDER BY start_time')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Opera')

                        opera_downloads = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        opera_downloads.append(column_name)
                        for index, tuple in enumerate(data):
                            opera_downloads.append(("Opera", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                                    tuple[6], tuple[7]))

                        with open('opera_downloads.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in opera_downloads:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA opera_downloads.js file has been created with [Browser, Download Timestamp, Last Accessed Timestamp, Received Bytes, Total_bytes, State(0/1), Download File Path, Download URL, Referrer] ordered by Download Timestamp \n')
                        return (opera_downloads)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "history" or artifact_input == "History":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Roaming\Opera Software\Opera Stable\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls ORDER BY last_visit_timestamp')
                data = cur.fetchall()

                cur.execute(
                    'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls ORDER BY visit_count DESC LIMIT 50')
                visit_count_data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Opera')

                print('The top 50 most visited sites:\n')
                print(column_name, '\n')
                for i in visit_count_data:
                    print(i)

                opera_history = []  # creating a list with the browser tag that can be returned for merging artifacts later
                opera_history.append(column_name)
                for index, tuple in enumerate(data):
                    opera_history.append(("Opera", tuple[0], tuple[1], tuple[2], tuple[3]))

                with open('opera_history.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in opera_history:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA opera_history.js file has been created with [Browser, Last Visit Timestamp, Visit Count, Url] ordered by Last Visit Timestamp. \n')
                return (opera_history)
            except Exception as err:
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls ORDER BY last_visit_timestamp')
                        data = cur.fetchall()

                        cur.execute(
                            'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls ORDER BY visit_count DESC LIMIT 50')
                        visit_count_data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Opera')

                        print('The top 50 most visited sites:\n')
                        print(column_name, '\n')
                        for i in visit_count_data:
                            print(i)

                        opera_history = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        opera_history.append(column_name)
                        for index, tuple in enumerate(data):
                            opera_history.append(("Opera", tuple[0], tuple[1], tuple[2], tuple[3]))

                        with open('opera_history.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in opera_history:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA opera_history.js file has been created with [Browser, Last Visit Timestamp, Visit Count, Url] ordered by Last Visit Timestamp. \n')
                        return (opera_history)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "logins" or artifact_input == "Logins":
            try:
                con = sqlite3.connect(
                    r"C:\Users\{}\AppData\Roaming\Opera Software\Opera Stable\Login Data".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                    'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                    ' username_value, origin_url'
                    ' FROM logins ORDER BY login_date_created')
                data = cur.fetchall()

                cur.execute(
                    'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                    'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                    ' username_value, origin_url'
                    ' FROM logins ORDER BY times_used DESC LIMIT 50')
                times_used_count_data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Opera')

                print('The top 50 most used logins:\n')
                print(column_name, '\n')
                for i in times_used_count_data:
                    print(i)

                opera_logins = []  # creating a list with the browser tag that can be returned for merging artifacts later
                opera_logins.append(column_name)
                for index, tuple in enumerate(data):
                    opera_logins.append(("Opera", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))
                # items with incorrect timestamps (1601 00:00:00 etc) are so because the values on the table are null/0
                with open('opera_logins.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in opera_logins:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA opera_logins.js file has been created with [Browser, Download Timestamp, Download File Path, Download URL] ordered by Download Timestamp \n')
                return (opera_logins)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                            'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                            ' username_value, origin_url'
                            ' FROM logins ORDER BY login_date_created')
                        data = cur.fetchall()

                        cur.execute(
                            'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                            'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                            ' username_value, origin_url'
                            ' FROM logins ORDER BY times_used DESC LIMIT 50')
                        times_used_count_data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Opera')

                        print('The top 50 most used logins:\n')
                        print(column_name, '\n')
                        for i in times_used_count_data:
                            print(i)

                        opera_logins = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        opera_logins.append(column_name)
                        for index, tuple in enumerate(data):
                            opera_logins.append(("Opera", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))
                        # items with incorrect timestamps (1601 00:00:00 etc) are so because the values on the table are null/0
                        with open('opera_logins.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in opera_logins:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA opera_logins.js file has been created with [Browser, Download Timestamp, Download File Path, Download URL] ordered by Download Timestamp \n')
                        return (opera_logins)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "keywords" or artifact_input == "Keywords":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Roaming\Opera Software\Opera Stable\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute('SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp,'
                    'term AS searched_keywords, url FROM keyword_search_terms LEFT JOIN urls ON keyword_search_terms.url_id = urls.id')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Opera')

                opera_keywords = []  # creating a list with the browser tag that can be returned for merging artifacts later
                opera_keywords.append(column_name)
                for index, tuple in enumerate(data):
                    opera_keywords.append(("Opera", tuple[0], tuple[1], tuple[2]))

                with open('opera_keywords.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in opera_keywords:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA opera_keywords.js file has been created with [Keywords searched, urls]. \n')
                return (opera_keywords)
            except Exception as err:
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute('SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp,'
                    'term AS searched_keywords, url FROM keyword_search_terms LEFT JOIN urls ON keyword_search_terms.url_id = urls.id')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Opera')

                        opera_keywords = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        opera_keywords.append(column_name)
                        for index, tuple in enumerate(data):
                            opera_keywords.append(("Opera", tuple[0], tuple[1], tuple[2]))

                        with open('opera_keywords.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in opera_keywords:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA opera_keywords.js file has been created with [Keywords searched, urls]. \n')
                        return (opera_keywords)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1

#Function in charge of retrieving edge artifacts
def edge():
    user = os.getlogin()
    max_count = 3
    count = 0
    while True:  # keeps the function going even after a successful output in case the user wants to analyse another artifact, only if the function is presented with an "exit" it'll go back to main()
        print(
            '\nWhich web browser artifact would you like to analyse? \n[Cookies, History, Downloads, Logins, Keywords (search terms)..] - or \'exit\' \n')
        artifact_input = input()
        if artifact_input == 'exit':
            break
        else:
            pass
        if artifact_input == "cookies" or artifact_input == "Cookies":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Microsoft\Edge\User Data\Profile 1\Cookies".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                # Edge's base time is 01/01/1601 00:00:00.
                # To calculate local time, Edge time has to be converted to seconds by dividing by one-million,
                # and then the seconds differential between 01/01/1601 00:00:00 and 01/01/1970 00:00:00 must be subtracted

                cur.execute(
                    'SELECT datetime(creation_utc / 1e6 - 11644473600, "unixepoch") AS creation_timestamp,'
                    ' datetime(last_access_utc / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp,'
                    'is_secure, is_httponly, is_persistent, priority, samesite, host_key, name '
                    ' FROM cookies ORDER BY creation_utc')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Edge')

                edge_cookies = []  # creating a list with the browser tag that can be returned for merging artifacts later
                edge_cookies.append(column_name)
                for index, tuple in enumerate(data):
                    edge_cookies.append(("Edge", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                           tuple[6], tuple[7], tuple[8]))

                with open('edge_cookies.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in edge_cookies:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA edge_cookies.js file has been created with [Browser, Cookie creation timestamp, Cookie Last Access Timestamp,is_secure, is_httponly, is_persistent, priority, samesite, Host Key, Cookie Name] ordered by Cookie Creation Timestamp\n')
                return (edge_cookies)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(creation_utc / 1e6 - 11644473600, "unixepoch") AS creation_timestamp,'
                            ' datetime(last_access_utc / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp,'
                            'is_secure, is_httponly, is_persistent, priority, samesite, host_key, name '
                            ' FROM cookies ORDER BY creation_utc')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Edge')

                        edge_cookies = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        edge_cookies.append(column_name)
                        for index, tuple in enumerate(data):
                            edge_cookies.append(("Edge", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                                   tuple[6], tuple[7], tuple[8]))

                        with open('edge_cookies.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in edge_cookies:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA edge_cookies.js file has been created with [Browser, Cookie creation timestamp, Cookie Last Access Timestamp,is_secure, is_httponly, is_persistent, priority, samesite, Host Key, Cookie Name] ordered by Cookie Creation Timestamp\n')
                        return (edge_cookies)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "downloads" or artifact_input == "Downloads":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Microsoft\Edge\User Data\Profile 1\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(start_time / 1e6 - 11644473600, "unixepoch") AS download_start_timestamp,'
                    'datetime(last_access_time / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp, received_bytes, total_bytes, state,'
                    'current_path, url, referrer FROM downloads LEFT JOIN downloads_url_chains '
                    'ON downloads.id = downloads_url_chains.id ORDER BY start_time')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Edge')

                edge_downloads = []  # creating a list with the browser tag that can be returned for merging artifacts later
                edge_downloads.append(column_name)
                for index, tuple in enumerate(data):
                    edge_downloads.append(("Edge", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                             tuple[6], tuple[7]))

                with open('edge_downloads.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in edge_downloads:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA edge_downloads.js file has been created with [Browser, Download Timestamp, Last Modified, Received Bytes, Total_bytes, State(0/1), Download File Path, Download URL, Referrer] ordered by Download Timestamp \n')
                return (edge_downloads)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(start_time / 1e6 - 11644473600, "unixepoch") AS download_start_timestamp,'
                            'datetime(last_access_time / 1e6 - 11644473600, "unixepoch") AS last_access_timestamp, received_bytes, total_bytes, state,'
                            'current_path, url, referrer FROM downloads LEFT JOIN downloads_url_chains '
                            'ON downloads.id = downloads_url_chains.id ORDER BY start_time')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Edge')

                        edge_downloads = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        edge_downloads.append(column_name)
                        for index, tuple in enumerate(data):
                            edge_downloads.append(
                                ("Edge", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5],
                                 tuple[6], tuple[7]))

                        with open('edge_downloads.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in edge_downloads:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA edge_downloads.js file has been created with [Browser, Download Timestamp, Last Modified, Received Bytes, Total_bytes, State(0/1), Download File Path, Download URL, Referrer] ordered by Download Timestamp \n')
                        return (edge_downloads)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "history" or artifact_input == "History":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Microsoft\Edge\User Data\Profile 1\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls ORDER BY last_visit_timestamp')
                data = cur.fetchall()

                cur.execute(
                    'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls ORDER BY visit_count DESC LIMIT 50')
                visit_count_data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Edge')

                print('The top 50 most visited sites:\n')
                print(column_name, '\n')
                for i in visit_count_data:
                    print(i)

                edge_history = []  # creating a list with the browser tag that can be returned for merging artifacts later
                edge_history.append(column_name)
                for index, tuple in enumerate(data):
                    edge_history.append(("Edge", tuple[0], tuple[1], tuple[2], tuple[3]))

                with open('edge_history.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in edge_history:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA edge_history.js file has been created with [Browser, Last Visit Timestamp, Visit Count, Url] ordered by Last Visit Timestamp. \n')
                return (edge_history)
            except Exception as err:
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp,'
                            ' visit_count, url, title FROM urls ORDER BY last_visit_timestamp')
                        data = cur.fetchall()

                        cur.execute(
                            'SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp, visit_count, url, title FROM urls ORDER BY visit_count DESC LIMIT 50')
                        visit_count_data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Edge')

                        print('The top 50 most visited sites:\n')
                        print(column_name, '\n')
                        for i in visit_count_data:
                            print(i)

                        edge_history = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        edge_history.append(column_name)
                        for index, tuple in enumerate(data):
                            edge_history.append(("Edge", tuple[0], tuple[1], tuple[2], tuple[3]))

                        with open('edge_history.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in edge_history:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA edge_history.js file has been created with [Browser, Last Visit Timestamp, Visit Count, Url] ordered by Last Visit Timestamp. \n')
                        return (edge_history)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "logins" or artifact_input == "Logins":
            try:
                con = sqlite3.connect(
                    r"C:\Users\{}\AppData\Local\Microsoft\Edge\User Data\Profile 1\Login Data".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute(
                    'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                    'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                    ' username_value, origin_url'
                    ' FROM logins ORDER BY login_date_created')
                data = cur.fetchall()

                cur.execute(
                    'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                    'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                    ' username_value, origin_url'
                    ' FROM logins ORDER BY times_used DESC LIMIT 50')
                times_used_count_data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Edge')

                print('The top 50 most used logins:\n')
                print(column_name, '\n')
                for i in times_used_count_data:
                    print(i)

                edge_logins = []  # creating a list with the browser tag that can be returned for merging artifacts later
                edge_logins.append(column_name)
                for index, tuple in enumerate(data):
                    edge_logins.append(("Edge", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))
                # items with incorrect timestamps (1601 00:00:00 etc) are so because the values on the table are null/0
                with open('edge_logins.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in edge_logins:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA edge_logins.js file has been created with [Browser, Download Timestamp, Download File Path, Download URL] ordered by Download Timestamp \n')
                return (edge_logins)
            except Exception as err:  # This exception catches wrong path files and asks user to input a different one on their own
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute(
                            'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                            'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                            ' username_value, origin_url'
                            ' FROM logins ORDER BY login_date_created')
                        data = cur.fetchall()

                        cur.execute(
                            'SELECT datetime(date_created / 1e6 - 11644473600, "unixepoch") AS login_date_created, times_used,'
                            'datetime(date_last_used / 1e6 - 11644473600, "unixepoch") AS login_date_last_used, '
                            ' username_value, origin_url'
                            ' FROM logins ORDER BY times_used DESC LIMIT 50')
                        times_used_count_data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Edge')

                        print('The top 50 most used logins:\n')
                        print(column_name, '\n')
                        for i in times_used_count_data:
                            print(i)

                        edge_logins = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        edge_logins.append(column_name)
                        for index, tuple in enumerate(data):
                            edge_logins.append(("Edge", tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))

                        with open('edge_logins.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in edge_logins:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA edge_logins.js file has been created with [Browser, Download Timestamp, Download File Path, Download URL] ordered by Download Timestamp \n')
                        return (edge_logins)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1
        elif artifact_input == "keywords" or artifact_input == "Keywords":
            try:
                con = sqlite3.connect(r"C:\Users\{}\AppData\Local\Microsoft\Edge\User Data\Profile 1\History".format(user))
                cur = con.cursor()
                con.text_factory = lambda b: b.decode(
                    errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                cur.execute('SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp,'
                    'term AS searched_keywords, url FROM keyword_search_terms LEFT JOIN urls ON keyword_search_terms.url_id = urls.id')
                data = cur.fetchall()

                # inserting sql column names to the list
                column_name = [i[0] for i in cur.description]
                column_name.insert(0, 'Browser: Edge')

                edge_keywords = []  # creating a list with the browser tag that can be returned for merging artifacts later
                edge_keywords.append(column_name)
                for index, tuple in enumerate(data):
                    edge_keywords.append(("Edge", tuple[0], tuple[1], tuple[2]))

                with open('edge_keywords.js',
                          'w') as f:  # w to write over stuff, a to append/add to what's already there
                    for row in edge_keywords:
                        f.write('\n')
                        json.dump(row, f)
                f.close()
                con.close()
                print(
                    '\nA edge_keywords.js file has been created with [Keywords searched, urls]. \n')
                return (edge_keywords)
            except Exception as err:
                print("[+] - " + str(
                    err) + "- Either the default path files were modified, you don't have the right web browser installed or your browser is currently open - [+]\n")
                count = 0  # count definition is here so that it gets reset if this artifact is called again for analysis (just in case)
                while True and count < max_count:  # This makes it so it doesn't jump into the next function in main() right away
                    try:
                        print("[+] - If modified, please type in the correct file path - or 'exit' - [+]")
                        url_input = input()
                        if url_input == "exit":  # If condition to break out of the while true loop
                            break
                        else:
                            pass
                        con = sqlite3.connect(url_input)
                        cur = con.cursor()
                        con.text_factory = lambda b: b.decode(
                            errors="ignore")  # ignore utf-8 encoding errors from one of the database columns
                        cur.execute('SELECT datetime(last_visit_time / 1e6 - 11644473600, "unixepoch") AS last_visit_timestamp,'
                    'term AS searched_keywords, url FROM keyword_search_terms LEFT JOIN urls ON keyword_search_terms.url_id = urls.id')
                        data = cur.fetchall()

                        # inserting sql column names to the list
                        column_name = [i[0] for i in cur.description]
                        column_name.insert(0, 'Browser: Edge')

                        edge_keywords = []  # creating a list with the browser tag that can be returned for merging artifacts later
                        edge_keywords.append(column_name)
                        for index, tuple in enumerate(data):
                            edge_keywords.append(("Edge", tuple[0], tuple[1], tuple[2]))

                        with open('edge_keywords.js',
                                  'w') as f:  # w to write over stuff, a to append/add to what's already there
                            for row in edge_keywords:
                                f.write('\n')
                                json.dump(row, f)
                        f.close()
                        con.close()
                        print(
                            '\nA edge_keywords.js file has been created with [Keywords searched, urls]. \n')
                        return (edge_keywords)
                    except Exception as err:
                        print("[+] - " + str(
                            err) + " - Wrong path file or incorrect data format - Check if it's an SQLite database file")
                        count += 1


if __name__ == '__main__':
    main()
