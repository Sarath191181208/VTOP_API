from typing import Dict, List
import pandas as pd

def parse_single_subject_attendance(single_subject_attd_html: str) -> List[Dict[str, str]]:
    attd_tb = pd.read_html(single_subject_attd_html)[1]
    attd_tb["Attendance Date"] = pd.to_datetime(attd_tb['Date'], format='%d-%m-%Y').dt.strftime('%d-%b-%Y')
    attd_tb = attd_tb.rename(columns={
        "Slot" : "Attendance Slot",
        "Status" : "Attendance Status",
        "Day / Time" : "Day And Timing"
    })
    attd_tb = attd_tb.drop(columns=["Sl.No.", "Date"])
    return attd_tb.to_dict(orient='records')
