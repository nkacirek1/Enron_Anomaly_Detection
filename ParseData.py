import os
from email.parser import Parser

rootdir = "/Users/girikranchhod/School/CS445/term_project/input/maildir"


def parse_email(inputfile, to_email_list, from_email_list, date_list):
    with open(inputfile, "r", encoding='latin-1') as f:
        data = f.read()

    email = Parser().parsestr(data)

    if email['to']:
        email_to = email['to']
        email_to = email_to.replace("\n", "")
        email_to = email_to.replace("\t", "")
        email_to = email_to.replace(" ", "")
        email_to = email_to.split(",")

        for email_to_1 in email_to:
            to_email_list.append(email_to_1)

    from_email_list.append(email['from'])
    date_list.append(email['date'])


to_email_list = []
from_email_list = []
date_list = []

month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
              "Nov": 11,
              "Dec": 12}

file = open("enron.csv", "w+")

for directory, subdirectory, filenames in os.walk(rootdir):
    for filename in filenames:
        parse_email(os.path.join(directory, filename), to_email_list, from_email_list, date_list)

for to_email, from_email, date_email in zip(to_email_list, from_email_list, date_list):
    date = date_email.split('-')[0][:-10]
    date = date[5:]
    dayMonthYear = date.split(' ')
    day = str(dayMonthYear[0])
    month = str(month_dict[dayMonthYear[1]])
    year = str(dayMonthYear[2])
    date = str(day) + '/' + str(month) + '/' + str(year)
    time = date_email.split('-')[0].split(' ')[4]
    file.write(
        to_email + ',' +
        from_email + ',' +
        day + ',' +
        month + ',' +
        year + ',' +
        time.split(':')[0] + '\n')
