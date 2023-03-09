import pandas as pd

from ..utils import nan_to_none_in_dict


def parse_marks_page(sub_details_html: str):
    """
        returns 
        [
            {
                "ClassNbr": "AP2022236000024",
                "Course Code": "MAT1011",
                "Course Title": "Applied Statistics",
                "Course Type": "Embedded Theory",
                "Course System": "FFCS",
                "Faculty": "Prof.Tanuj Kumar",
                "Slot": "B1+TB1",
                "Course Mode": "CBL",
                "marks": [
                    {
                        "Mark Title": "CAT-1",
                        "Max. Mark": "50",
                        "Weightage %": "20",
                        "Status": "Present",
                        "Scored Mark": "36",
                        "Weightage Mark": "14.4",
                        "Class Average": NaN,
                        "Mark Posted Strength": NaN,
                        "Remark": NaN
                    }
                    ...
                ]
            },
    ]
    """
    sub_details_tables = pd.read_html(sub_details_html)
    sub_details = sub_details_tables[0]
    # extract odd rows from sub_details
    sub_details_odd = sub_details.iloc[1::2, :]
    header = sub_details.iloc[0, :]  # extract header from sub_details
    sub_details_odd.columns = header  # set header as column names
    sub_details_odd = sub_details_odd.drop(
        columns=["Sl.No."])  # drop Sl.No. column
    sub_details_odd_dict = sub_details_odd.to_dict(
        orient="records")  # convert to list of dicts

    marks_list = []
    for table in sub_details_tables[1:]:
        table.columns = table.iloc[0, :]
        table = table.drop(index=0,)
        table = table.drop(columns=["Sl.No."])
        marks_list.append(tuple(
            nan_to_none_in_dict(item) for item in table.to_dict(orient="records")))  # type: ignore

    # merge the dicts in sub_details_odd and marks_dict
    for i, sub_detials in enumerate(sub_details_odd_dict):
        sub_detials["marks"] = marks_list[i]
    return sub_details_odd_dict # type: ignore
