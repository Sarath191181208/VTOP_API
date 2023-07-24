import pandas as pd
from bs4 import BeautifulSoup


import datetime
from typing import Dict

def get_sub_ids(attd_html: str) -> Dict[str, str]:
    """
        returns the list of subject ids from the attendance html
        the subject ids are in a .btn-link element in onclick
        Returns:
        --- 
            Dict[str, str]: a dictionary of slots and subject ids
            ex:
                {
                    "B1+TB1+TBB1": "AP2023241000001",
                    "B2+TB2+TBB2": "AP2023241000002",
                }
    """

    # use beautiful soup to get the subject ids
    soup = BeautifulSoup(attd_html, 'html.parser')
    slot_subid_dict = dict()
    for link in soup.find_all('a', {'class': 'btn-link'}):
        on_click_str = link.get('onclick')
        # on_click_str = javascript:processViewAttendanceDetail('AP2023241000001','B1+TB1+TBB1');
        # filter out AP2023241000001 and B1+TB1+TBB1
        sub_id = on_click_str.split("'")[1]
        slot = on_click_str.split("'")[3]
        slot_subid_dict[slot] = sub_id
    
    return slot_subid_dict



def parse_attendance(attendance_html: str) -> Dict[str, Dict] :
    """
        Parses the attendance html and returns a dictionary of attendance details.
        :check student attendance.py for more details on the structure of the dictionary.
    """

    raw_df = pd.read_html(attendance_html)
    df = raw_df[0]
    # removing redundant spaces in cols
    df.columns = [' '.join(str(col).strip().split()) for col in df.columns]

    slot_subid_dict = get_sub_ids(attendance_html)

    # create a column for subject ids and fill it with the subject ids
    df['Subject ID'] = df['Slot'].apply(lambda x: slot_subid_dict.get(x, None))


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
            "subjectID" : df.iloc[row]['Subject ID'],
            "updatedOn" : datetime.datetime.now().strftime("%c")
        }
    # print(attendace_dict)
    return attendace_dict