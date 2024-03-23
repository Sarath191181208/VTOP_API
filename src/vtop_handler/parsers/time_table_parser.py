
from typing import Dict, List
from bs4 import BeautifulSoup
import pandas as pd


def _get_course_code_dic(df) -> Dict[str, str]:
    """ creating a dictionary of course code and course name ex: 
        {
            "ECE4008": "Computer Communication",
            "ECE4015": "Data Structures",
        }
    """
    _df = df[0]
    _df[["Course Code","Course Name"]] = _df['Course'].str.split('-', n=1, expand=True)
    _df["Course Code"] = _df["Course Code"].str.strip()
    _df["Course Name"] = _df["Course Name"].str.strip()
    return dict(_df[["Course Code", "Course Name"]].to_dict("split")["data"])
 


def parse_timetable(timetable_html: str) -> Dict[str, List]:
    """takes the html of the timetable and returns the timetable in the form of a dictionary"""
    def _get_vals(s):  # temporary helper function
        """ gets the solt course code and class name for a row """
        temp_arr = str(s).strip().split("-")
        slot = temp_arr[0]
        course_code = temp_arr[1]
        cls = "-".join(temp_arr[3:])

        return slot, course_code, cls

    time_table = {"Monday": [], "Tuesday": [], "Wednesday": [],
                  "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}
    # helper dictionary to convert from short form to longer one
    _temp_dic = {"MON": "Monday", "TUE": 'Tuesday', "WED": 'Wednesday',
                 "THU": 'Thursday', "FRI": 'Friday', "SAT": "Saturday", "SUN": "Sunday"}

    # for the time table we have two tables one's with the course lectures and the other with the scheduled classes
    raw_df = pd.read_html(timetable_html)
    df = raw_df[1]

    course_code_name_dic = _get_course_code_dic(raw_df[0])

    # iterating over the rows of the table and converting to json format
    for row_idx in range(3, df.shape[0]):
        # The second col i.e idx 1 in data is the theory or lab
        is_theory = (df.iloc[row_idx, 1] == 'Theory')
        # The second col in data is the day of the week
        # The day is in short form i.e "TUE" we need to convert it to "Tuesday"
        day = _temp_dic.get(str(df.iloc[row_idx, 0]), "Sunday")

        for col_idx in range(2, df.shape[1]):
            cell = df.iloc[row_idx, col_idx]
            cell_str = str(cell).strip()
            is_cell_empty = cell_str.count(
                '-') < 3 or len(cell_str) <= 3 or all([char == '-' for char in cell_str])
            # if the cell is empty without data then we skip it
            if not is_cell_empty:
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
