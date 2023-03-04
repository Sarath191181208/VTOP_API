import pandas as pd


import datetime
from typing import Dict


def parse_attendance(attendance_html: str) -> Dict[str, Dict] :
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