import pandas as pd
from bs4 import BeautifulSoup


from typing import Dict, List


def parse_acadhistory(acad_html: str)-> Dict[str, List]:

    # if the student has no academic history 
    soup = BeautifulSoup(acad_html, "lxml")
    txt = soup.select('form > div > h3')
    if len(txt) > 0 and txt[0].text.replace(" ", '') == "NoRecordsFound":
        return { "summary": [], "subjects": [] }

    # actual parsing starts here
    raw_df = pd.read_html(acad_html)

    grades_df = raw_df[1].copy()
    summary_df = raw_df[-1].copy()
    # convering summary to dict
    cols = summary_df.columns
    dic = {"summary":{k.replace(" ", "").replace("Grades", "") : float(summary_df.iloc[0][k]) for k in cols[:-1]}} # type: ignore
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
    return dic | grades_df.to_dict() # type: ignore
