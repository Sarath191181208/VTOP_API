from typing import Dict
import aiohttp

from .payloads import get_course_page_semeseter_names_payload
from .constants import COURSE_PAGE_URL, HEADERS
from .parsers import parse_course_page_semester_names

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
        with open('course_page.html', 'w') as f:
            f.write(html)
        try:
            return_data = parse_course_page_semester_names(html)
        except Exception as e:
            print(e)
            print(e.__traceback__)
        finally:
            return return_data