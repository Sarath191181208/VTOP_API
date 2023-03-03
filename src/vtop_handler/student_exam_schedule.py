"""
Returns Timetable in a dictionary form

    Usage:
    ------
    > import asyncio, aiohttp
    > from vtop_handler.session_generator import get_valid_session
    > form vtop_handler.student_timetable import get_exam_schedule 
    >
    > async def main():
    >     async with aiohttp.ClientSession() as sess:
    >         user_name, valid = await get_valid_session(user_name, password, sess)
    >         exam_schedule, valid = await get_exam_schedule(sess, user_name)
    >         print(exam_schedule)
    > 
    > if __name__ == "__main__":
    >     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    >     asyncio.run(main())

"""
from typing import Tuple

from .constants import VTOP_EXAM_SCHEDULE_URL, HEADERS, SEM_IDS
from .payloads import get_exam_schedule_payload 
from .parsers import parse_exam_schedule

import asyncio
import aiohttp

async def _get_exam_schedule_from_payload(sess:aiohttp.ClientSession, payload:dict) -> Tuple[dict, bool]:
    """
        Returns the timetable of the user in the form of a dictionary using the payload given
        which is mentioned above in the file containing this function.
    """

    valid = False
    exam_schedule = {}
    
    async with sess.post(VTOP_EXAM_SCHEDULE_URL, data=payload, headers=HEADERS) as resp:
        timetable_html = await resp.text()
        if resp.status == 200:
            try: 
                exam_schedule = parse_exam_schedule(timetable_html)
                valid = True
            except Exception as e:
                print(f"payload: {payload}")
                print("Error in parsing the exam schdule with error: ", e)
        else:
            print("Error in getting exam schedule with payload: ", payload)

    return (exam_schedule, valid)

async def get_exam_schedule(
    sess: aiohttp.ClientSession, 
    username: str,
    semesterID: str = None) -> Tuple[
        dict,  # exam schedule
        bool]: # valid i.e sucess of the session
    """
        Gets the examschedule of the user for the given semesterID using the given session & username

        Parameters:
        -----------
        sess: aiohttp.ClientSession
            the session to use for the request
        username: str
            the username of the user
        semesterID: str
            the semesterID of the user

        Returns:
        --------
        exam_schedule: dict
            the exam schedule of the user in the form of a dictionary
            {
                |
                |
                |
            }
        valid: bool
            whether the request was successful or not
    """

    # TODO calling the api with the semesterID is to be implemented
    
    valid = False
    exam_sch = {}
    for semID in set(SEM_IDS):
        payload = get_exam_schedule_payload(username, semID)
        exam_sch, valid = await _get_exam_schedule_from_payload(sess, payload)
        if valid:
            break

    return (exam_sch, valid)
