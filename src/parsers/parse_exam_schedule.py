from src.vtop_handler.utils import is_int, null_if_dash

import pandas as pd
from collections import defaultdict
from typing import Dict


def get_exam_row_data(row):
    data = {
        "Course Code": row[1],
        "Course Title": row[2],
        "Class ID": row[4],
        "Slot": row[5],
        "Exam Date": row[6],
        "Reporting Time": row[8],
        "Exam Time": row[9],
        "Venue Block":  null_if_dash(row[10]),
        "Venue Room":   null_if_dash(row[11]),
        "Seat Location": null_if_dash(row[12]),
        "Seat No":      null_if_dash(row[13]),
    }
    #  connvert  NaN to None
    data = {k: None if pd.isna(v) else v for k, v in data.items()}
    return data

def parse_exam_schedule(exam_schedule_html: str) -> Dict:
    dfs = pd.read_html(exam_schedule_html)
    exam_schedule_data = defaultdict(list)
    curr_exam = None

    for row in dfs[0][1:].iterrows():
        if not is_int(row[1][0]): curr_exam = row[1][0]
        elif curr_exam is None: continue
        else: exam_schedule_data[curr_exam].append(get_exam_row_data(row[1]))

    return exam_schedule_data