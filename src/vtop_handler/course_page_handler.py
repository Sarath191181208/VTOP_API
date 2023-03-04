from typing import Dict, List
import aiohttp

from .payloads import get_course_page_semeseter_names_payload, get_course_page_subject_names_payload, get_course_page_table_of_contents_payload
from .constants import COURSE_PAGE_URL, COURSE_PAGE_SEMESTER_URL, COURSE_PAGE_SELECT_COURSE_URL, HEADERS
from .parsers import parse_course_page_semester_names, parse_course_names_values, parse_to_get_view_urls

def may_throw(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__} with args: {args} and kwargs: {kwargs}")
            print(f"Error: {e}")
    return wrapper

@may_throw
async def get_course_semesters_list(sess: aiohttp.ClientSession, auth_id: str) -> Dict[str, str]:
    """
        Return a dict of all the text of the option element inturn the semester names

        Returns:
        ---
        {
            'AP2022237': 'WIN SEM (2022-23) Freshers - AMR',
            'AP2022236': 'WIN SEM (2022-23) - AMR',
            ...
        }
    """

    return_data = {}
    payload = get_course_page_semeseter_names_payload(auth_id)
    async with sess.post(COURSE_PAGE_URL, data=payload, headers=HEADERS) as resp:
        html = await resp.text()
        return_data = parse_course_page_semester_names(html)
        return return_data

@may_throw
async def get_course_page(sess: aiohttp.ClientSession, auth_id: str, semester_id: str) -> Dict[str, str]:
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
    payload = get_course_page_subject_names_payload(semester_id, auth_id)
    async with sess.post(COURSE_PAGE_SEMESTER_URL, data=payload, headers=HEADERS) as resp:
        html =  await resp.text()
        return parse_course_names_values(html)


@may_throw
async def get_course_page_links_payload(sess: aiohttp.ClientSession, class_id: str, semester_id: str, auth_id: str) -> List[Dict[str, str]]:
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
    payload = get_course_page_table_of_contents_payload(
        class_id, semester_id, auth_id)
    async with sess.post(COURSE_PAGE_SELECT_COURSE_URL, data=payload, headers=HEADERS) as resp:
        html = await resp.text()
        return parse_to_get_view_urls(html)
