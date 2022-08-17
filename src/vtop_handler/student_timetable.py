"""
Returns Timetable in a dictionary form

    Usage:
    ------
    > import asyncio, aiohttp
    > from vtop_handler.session_generator import get_valid_session
    > form vtop_handler.student_timetable improt get_timetable
    >
    > async def main():
    >     async with aiohttp.ClientSession() as sess:
    >         user_name, valid = await get_valid_session(user_name, password, sess)
    >         time_table, valid = await get_timetable(sess, user_name)
    >         print(time_table)
    > 
    > if __name__ == "__main__":
    >     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    >     asyncio.run(main())

"""
from typing import Tuple

from .constants import VTOP_TIMETABLE_URL, HEADERS, SEM_IDS
from .payloads import get_vtop_timetable_payload 
from .parsers import parse_timetable

import asyncio
import aiohttp

async def _get_time_table_from_payload(sess:aiohttp.ClientSession, payload:dict) -> Tuple[dict, bool]:
    """
        Returns the timetable of the user in the form of a dictionary using the payload given
        which is mentioned above in the file containing this function.
    """

    valid = False
    time_table = {}
    
    async with sess.post(VTOP_TIMETABLE_URL, data=payload, headers=HEADERS) as resp:
        timetable_html = await resp.text()
        if resp.status == 200:
            try: 
                time_table = parse_timetable(timetable_html)
                valid = True
            except Exception as e:
                print(f"payload: {payload}")
                print("Error in parsing the timetable with error: ", e)
        else:
            print("Error in getting timetable with payload: ", payload)

    return (time_table, valid)

async def get_timetable(
    sess: aiohttp.ClientSession, 
    username: str,
    semesterID: str = None) -> Tuple[
        dict,  # timetable
        bool]: # valid i.e sucess of the session
    """
        Gets the timetable of the user for the given semesterID using the given session & username

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
        time_table: dict[str, list]
            the time table of the user in the given semesterID
            time_table =  {
                "Monday": [
                |    
                |    {
                |    |    "slot" : "A1",
                |    |    "courseName" : "Computer Communication",
                |    |    "code" : "ECE4008",
                |    |    "class" : "AB1 408",
                |    |    startTime: "8:00",
                |    |    endTime:"8:50"
                |    },
                |
                |    {
                |    |    "slot" : "A2",
                |    |    "courseName" : "Computer Communication",
                |    |    "code" : "ECE4008",
                |    |    "class" : "AB1 408",
                |    |    startTime: "9:00",
                |    |    endTime:"9:50"
                |    }
                ]
            }

        valid: bool
            whether the request was successful or not
    """

    # TODO calling the api with the semesterID is to be implemented
    
    valid = False
    time_table = {}
    for semID in set(*SEM_IDS):
        payload = get_vtop_timetable_payload(username, semID)
        time_table, valid = await _get_time_table_from_payload(sess, payload)
        if valid:
            break

    return (time_table, valid)
