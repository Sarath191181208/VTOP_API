

import bs4 as bs
from typing import Dict, List
import pandas as pd
from bs4 import BeautifulSoup
import re


def parse_course_page_semester_names(course_page_view_html: str) -> Dict[str, str]:
    """ 
        return a dict of all the text of the option element inturn the semester names

        Returns:
        ---
        {
            'AP2022237': 'WIN SEM (2022-23) Freshers - AMR',
            'AP2022236': 'WIN SEM (2022-23) - AMR',
            ...
        }
    """
    soup = BeautifulSoup(course_page_view_html, 'html.parser')
    options = soup.find_all('option')
    # return the list removing the first, last elements as they are placeholders -- Choose Semester --, -- Choose Faculty --
    options = options[1:-3]
    print(options)
    return {option['value']: option.text for option in options}


def parse_course_names_values(get_course_for_course_page_html: str) -> Dict[str, str]:
    """ 
        returns the dict of all the option element inturn the course names and values 

        Returns:
        ---
        {
            'AP2022236000502': 'CSE2007 - Database Management Systems - ETH', 
            'AP2022236000756': 'CSE2007 - Database Management Systems - ELA', 
            ...
        }
    """
    soup = BeautifulSoup(get_course_for_course_page_html, 'html.parser')
    options = soup.find_all('option')
    options = options[1:]  # remove the first as it's a placeholder
    return {option['value']: option.text for option in options}


def _zip_with_keys(values: List[str]) -> Dict[str, str]:
    keys = [
        "semSubId", "erpId", "courseType", "roomNumber",
        "buildingId", "slotName", "classId", "courseCode",
        "courseTitle", "allottedProgram", "classNum", "facultyName", "facultySchool", "courseId",
    ]
    return dict(zip(keys, values))


def parse_to_get_view_urls(full_course_page_html: str) -> List[Dict[str, str]]:
    """
        Returns the * payload * that's requrired to get the table of contents of a course
        Returns:
        ---
        {
            'semSubId': 'AP2022236000502',
            'erpId': 'AP2022236',
            ...
        }
    """
    # find all the buttons with onlick in a table
    soup = BeautifulSoup(full_course_page_html, 'html.parser')
    buttons = soup.find_all('button', {'onclick': True})
    buttons = [button['onclick'] for button in buttons]
    # using regex find the data which is like this javascript:processViewStudentCourseDetail( data );
    # pattern to find the data
    pattern = re.compile(
        r"javascript:processViewStudentCourseDetail\((.*?)\);")
    buttons = [re.findall(pattern, button)[0].replace("'", "").split(
        ",") for button in buttons]  # buttons: list[ list[str] ]
    # buttons: list[ dict[str, str] ]
    buttons = [_zip_with_keys(button) for button in buttons]
    return buttons


def _extract_link_from_href(href_text: str) -> str:
    pattern = re.compile(r"javascript:vtopDownload\('(.*?)'\)")
    return re.findall(pattern, href_text)[0]


def _read_html(html: str):
    soup = bs.BeautifulSoup(html, 'lxml')
    parsed_table = soup.find_all('table')[2]
    data = [[_extract_link_from_href(td.a['href']) if td.find('a') else
             ''.join(td.stripped_strings)
             for td in row.find_all('td')]
            for row in parsed_table.find_all('tr')]
    df = pd.DataFrame(data[1:], columns=data[0])

    return df


def parse_reference_material_links(full_course_page_html: str) -> List[Dict[str, str]]:
    """
    Parses the reference material links from the full course page html

    Returns:
    --- 
        [
            {
                'Lecture Date': '04-Jan-2023',
                'Lecture Topic': 'CO PO disussion',
                'Reference Material': ''
            },
            {
                'Lecture Date': '05-Jan-2023',
                'Lecture Topic': 'Introduction to data, information and knowledge',
                'Reference Material': 'downloadPdf/AP2022236/AP2022236000511/19/05-Jan-2023'
            },
        ]
    """
    table_of_contents = _read_html(full_course_page_html)

    lecture_topic = table_of_contents.columns[3]
    reference_material = table_of_contents.columns[4]
    # remove if leture topic and reference material are both empty string for each row
    table_of_contents = table_of_contents[(table_of_contents[lecture_topic] != "") | (
        table_of_contents[reference_material] != "")]
    # drop the 0th column as it's serial number
    table_of_contents = table_of_contents.drop(
        table_of_contents.columns[0], axis=1)
    # drop the Lecture Day column as it's not needed
    table_of_contents = table_of_contents.drop(
        table_of_contents.columns[1], axis=1)
    table_of_contents = table_of_contents.to_dict(orient="records")
    return table_of_contents  # type: ignore
