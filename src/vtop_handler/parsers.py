"""
    All the parsers for the vtop_handler which take a html string 
    and return a parsed object i.e extracting data from the html files
"""

import datetime
import base64
import pandas as pd
from bs4 import BeautifulSoup

def parse_profile(profile_html: str)-> dict:
    raw_df = pd.read_html(profile_html)
    df_personal_info = raw_df[0]
    df_proctor_info = raw_df[3]

    application_number = df_personal_info.iloc[1, 1]
    
    # Generating an API Token
    api_gen = application_number
    api_token = api_gen.encode('ascii')
    temptoken = base64.b64encode(api_token)
    token = temptoken.decode('ascii')

    return {
        "name": df_personal_info.iloc[2, 1],
        "branch": df_personal_info.iloc[20, 1],
        "program" : df_personal_info.iloc[19, 1],
        "regNo" : df_personal_info.iloc[17, 1],
        "appNo" : df_personal_info.iloc[1, 1],
        "school" : df_personal_info.iloc[21, 1],
        "email" : df_personal_info.iloc[31, 1],
        "proctorEmail" : df_proctor_info.iloc[7 , 1],
        "proctorName": df_proctor_info.iloc[2 , 1],
        'token': token
    }

def _get_course_code_dic(time_table_soup:BeautifulSoup)-> dict[str, str]:
    """ creating a dictionary of course code and course name ex: 
        {
            "ECE4008": "Computer Communication",
            "ECE4015": "Data Structures",
        }
    """
    
    course_labels_soup = time_table_soup.find_all('td', {'style': lambda s: 'padding: 3px; font-size: 12px; border-color: #3c8dbc;vertical-align: middle;text-align: left;' in s})
    # getting the course data i.e the course column in the first table
    course_labels = [i.getText().split("-") for i in course_labels_soup]

    # only taking the first two items i.e course code and course name ex: cse-101 and Computer Science
    _get_course_code = lambda course_label : course_label[0].strip() #helper function
    _get_course_name = lambda course_label : " ".join( # helper function
        [name.strip() for name in course_label[1:-1]])
    # creating a dictionary of course code and course name
    course_code_name_dic = { _get_course_code(course_label) : _get_course_name(course_label) 
        for course_label in course_labels}
    
    return course_code_name_dic

def parse_timetable(timetable_html: str)-> dict[str, list]:
    """takes the html of the timetable and returns the timetable in the form of a dictionary"""
    soup = BeautifulSoup(timetable_html, 'lxml')
    course_code_name_dic = _get_course_code_dic(time_table_soup=soup)

    def _get_vals(s): # temporary helper function
        """ gets the solt course code and class name for a row """
        temp_arr = str(s).strip().split("-")
        slot = temp_arr[0]
        course_code = temp_arr[1]
        cls = temp_arr[2]+" "+temp_arr[3]

        return slot,course_code, cls

    time_table = {"Monday":[],"Tuesday":[],"Wednesday":[],"Thursday":[],"Friday":[],"Saturday":[],"Sunday":[]}
    # helper dictionary to convert from short form to longer one
    _temp_dic = {"MON":"Monday", "TUE":'Tuesday', "WED":'Wednesday', "THU":'Thursday', "FRI":'Friday',"SAT":"Saturday", "SUN":"Sunday"}  

    # for the time table we have two tables one's with the course lectures and the other with the scheduled classes
    raw_df = pd.read_html(timetable_html)
    df = raw_df[1]

    # iterating over the rows of the table and converting to json format
    for row_idx in range(3, df.shape[0]):
        # The second col i.e idx 1 in data is the theory or lab
        is_theory = (df.iloc[row_idx, 1] == 'Theory')
        # The second col in data is the day of the week
        # The day is in short form i.e "TUE" we need to convert it to "Tuesday"
        day = _temp_dic.get(str(df.iloc[row_idx, 0]), "Sunday")

        for col_idx in range(2, df.shape[1]):
            # if the cell is empty without data then we skip it
            if str(df.iloc[row_idx, col_idx]).count('-') > 2:
                slot, code, cls = _get_vals(df.iloc[row_idx, col_idx])

                time_table[day].append({
                    "slot": slot,
                    "courseName": course_code_name_dic[code],
                    "code": code,
                    "class": cls,
                    "startTime": df.iloc[0, col_idx] if is_theory else df.iloc[2, col_idx],
                    "endTime": df.iloc[1, col_idx] if is_theory else df.iloc[3, col_idx],
                })

    return time_table

def parse_attendance(attendance_html: str) -> dict[str, dict] :
    """
        Parses the attendance html and returns a dictionary of attendance details.
        :check student attendance.py for more details on the structure of the dictionary.
    """

    raw_df = pd.read_html(attendance_html)
    df = raw_df[0]
    # removing redundant spaces in cols
    df.columns = [' '.join(str(col).strip().split()) for col in df.columns]

    attendace_dict = dict()
    # The last column is for credits
    for row in range(df.shape[0]-1):

        slot = df.iloc[row]['Slot']

        attendace_dict[slot] = {
            "attended" : df.iloc[row]['Attended Classes'],
            "total" : df.iloc[row]['Total Classes'],
            "percentage" : df.iloc[row]['Attendance Percentage'],
            "faculty" : df.iloc[row]["Faculty Name"],
            "courseName" : df.iloc[row]['Course Title'],
            "code" : df.iloc[row]['Course Code'],
            "type" : df.iloc[row]['Course Type'],
            "updatedOn" : datetime.datetime.now().strftime("%c")
        }
    # print(attendace_dict)
    return attendace_dict

def parse_acadhistory(acad_html: str)-> dict[str, list]:

    # if the student has no academic history 
    soup = BeautifulSoup(acad_html, "lxml")
    txt = soup.select('form > div > h3')
    if len(txt) > 0 and txt[0].text.replace(" ", '') == "NoRecordsFound":
        return { "summary": {}, "subjects": {} }

    # actual parsing starts here
    raw_df = pd.read_html(acad_html)

    grades_df = raw_df[1].copy()
    summary_df = raw_df[-1].copy()

    # cleaning summary df 
    cols = summary_df.iloc[0]
    summary_df.drop(0, axis=0, inplace=True)
    summary_df.columns = cols
    # convering summary to dict
    dic = {"summary":{k.replace(" ", "").replace("Grades", "") : float(summary_df.iloc[0][k]) for k in cols}}
    # getting the cols of the grades df
    cols = grades_df.iloc[1]
    # the first two rows are just repeated i.e ele's and col names
    grades_df.drop([0, 1], axis=0, inplace=True)
    # removing redundant spaces and setting the column names
    grades_df.columns = [" ".join(str(ele).split()) for ele in cols]
    # taking only the nessasary cols
    grades_df = grades_df[["Course Title", "Grade"]]
    # setting the index to the course title
    grades_df.set_index("Course Title", inplace=True)
    # changed dictionary will have the key as subjects and value as grade
    grades_df.columns = ["subjects"]
    # | is similar to + in lists
    return dic | grades_df.to_dict()
