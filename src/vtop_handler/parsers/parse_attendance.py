import pandas as pd
import datetime
from typing import Dict 

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
            "type" : df.iloc[row]['Course Type'],
            "subjectId" : df.iloc[row]['Subject ID'],
            "updatedOn" : datetime.datetime.now().strftime("%c")
        }
    return attendace_dict
