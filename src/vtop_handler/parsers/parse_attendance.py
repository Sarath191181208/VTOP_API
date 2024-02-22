import pandas as pd
import datetime
from typing import Dict 
from bs4 import BeautifulSoup 
import re

CourseCode = str | None # AM_CSE1005_00100
CourseType = str | None # ETH, ELA 
# pattern to extract text between () 
pattern = re.compile(r'\((.*?)\)')

def transform_fn(course_detail: str):
    """
    Extracts the course code, course title and course type from the course detail string.
    Returns a tuple of course code, course title and course type.
    """
    if course_detail.count("-") >= 3:
        parts = course_detail.split('-')
        return parts[0], '-'.join(parts[1:-1]), parts[-1]
    return course_detail.split('-') 

def parse_attendance(attendance_html: str) -> Dict[str, Dict] :
    """
        Parses the attendance html and returns a dictionary of attendance details.
        :check student attendance.py for more details on the structure of the dictionary.
    """

    raw_df = pd.read_html(attendance_html)
    df = raw_df[0]
    course_id, course_type_short = _extract_course_code_type_list(attendance_html)
    df["Course Id"] = course_id
    df["Course Type Short"] = course_type_short
    # removing redundant spaces in cols
    df.columns = [' '.join(str(col).strip().split()) for col in df.columns]
    # Splitting the data seperated by - into cols CSE1005 - Software Engineering - Embedded Theory
    df[["Course Code", "Course Title", "Course Type"]] = df["Course Detail"].apply(transform_fn).apply(pd.Series)
    # AP2023246001037 - A1+TA1 - G14
    df[["Subject ID", "Slot", "Room No"]] = df["Class Detail"].str.split("-", expand=True)

    attendace_dict = dict()
    # The last column is for credits
    for row in range(df.shape[0]-1):
        slot = df.iloc[row]['Slot']

        attendace_dict[slot] = {
            "attended" : df.iloc[row]['Attended Classes'],
            "total" : df.iloc[row]['Total Classes'],
            "percentage" : df.iloc[row]['Attendance Percentage'],
            "faculty" : df.iloc[row]["Faculty Detail"],
            "courseName" : df.iloc[row]['Course Title'],
            "code" : df.iloc[row]['Course Code'],
            "courseId" : df.iloc[row]['Course Id'],
            "courseShortType" : df.iloc[row]['Course Type Short'],
            "type" : df.iloc[row]['Course Type'],
            "subjectId" : df.iloc[row]['Subject ID'],
            "updatedOn" : datetime.datetime.now().strftime("%c")
        }
    return attendace_dict

def _extract_course_code_and_type(tr) -> tuple[CourseCode, CourseType]:
    # getting all the td's 
    tds = tr.find_all("td")
    # getting the class id from last td 
    last_td = tds[-1]
    # extracting onlick from the <td> <a> </a> </td>
    t = last_td.a["onclick"]
    # extracting ('AP2023246','21BCE9853','AM_CSE1005_00100','ETH')
    params = pattern.search(t)
    if params is None: 
        return (None, None)
    # getting the params as list 
    params_list = ( params.group()
                   .replace(")", "")
                   .replace("(", "")
                   .replace("'", "")
                   .split(","))
    # getting course_code, course_type 
    course_code = params_list[2]
    course_type = params_list[3]

    return course_code, course_type 

def _extract_course_code_type_list(html: str) -> tuple[list[CourseCode], list[CourseType]]:
    soup = BeautifulSoup(html)
    # getting all the tr's from page
    trs = soup.find_all("tr")
    # helper arrs for saving res
    course_code_list: list[CourseCode] = []
    course_type_list: list[CourseType] = []
    # finding all the tr's and not iterating header
    for tr in trs[1:]:
        try: 
            course_code, course_type = _extract_course_code_and_type(tr)
            course_code_list.append(course_code)
            course_type_list.append(course_type)
        except (IndexError, TypeError) as e:
            course_type_list.append(None)
            course_code_list.append(None)
    return (course_code_list, course_type_list)
