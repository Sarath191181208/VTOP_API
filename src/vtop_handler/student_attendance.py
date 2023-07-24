"""
    This function gets the attendance details, from the VTOP page. Returns a json object with 

    Usage:
    ------
    > import asyncio, aiohttp
    > from vtop_handler.session_generator import get_valid_session
    > from vtop_handler.student_attendance import get_attendance
    >
    > async def main():
    >     async with aiohttp.ClientSession() as sess:
    >         user_name, valid = await get_valid_session(user_name, password, sess)
    >         attendance, valid = await get_attendance(sess, user_name)
    >         print(attendance)
    > 
    > if __name__ == "__main__":
    >     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    >     asyncio.run(main())
"""

from .constants import HEADERS, VTOP_ATTENDANCE_URL, SEM_IDS, VTOP_SINGLE_SUBJECT_ATTENDANCE_URL
from .payloads import generate_payload_attendance_for_subject, get_attendance_payload
from .parsers import parse_attendance, parse_single_subject_attendance 

import asyncio
import aiohttp
from typing import Dict, List, Tuple, Union

async def _get_attendance_from_payload(sess:aiohttp.ClientSession, payload: Dict, username: str) -> Tuple[dict, bool]:
    """
        Returns the attendance of the user in the form of a dictionary using the payload given
        which is mentioned above in the file containing this function.
    """

    valid = False
    attendance = {}
    
    async with sess.post(VTOP_ATTENDANCE_URL, data=payload, headers=HEADERS) as resp:
        attendance_html = await resp.text()
        if resp.status == 200:
            try: 
                attendance = parse_attendance(attendance_html)
            
                # get the data for the subject ids 
                tasks = [
                    asyncio.create_task(
                        get_single_subject_attendance(
                    sess, username, attendance[slot].get("subjectId", None), slot))   
                    for slot in attendance.keys()
                ]

                # wait for all the tasks to complete
                await asyncio.gather(*tasks)

                # update the attendance dict with the data
                for slot, task in zip(attendance.keys(), tasks):
                    attendance[slot]["history"] = await task

                valid = True
            except Exception as e:
                print(f"payload: {payload}")
                print("Error in parsing the attendance with error: ", e)
        else:
            print("Error in getting attendance with payload: ", payload)

    valid = False if attendance == {} else valid
    return (attendance, valid)

async def get_attendance(sess, username, semesterID=None):
    """
        Returns the attendance of the user in the form of a dictionary.
        The dictionary is of the form 

        Parameters:
        -----------
        sess: aiohttp.ClientSession
            The session object to be used for making the request.
        username: str
            The username of the user whose attendance is to be fetched.
        semesterID: str
            The semester ID of the user whose attendance is to be fetched.

        Returns:
        --------
        attendance: dict
            The attendance of the user in the form of a dictionary.
                {
                |   "slot" : {
                |    |  "attended" : 18   // Attended classes
                |    |  "total" : 20     // Total classes
                |    |  "pecentage" : 90 // Round off % from VTOp
                |    |  "faculty" : "AMIT KUMAR TYAGI"  // Faculty details
                |    |  "courseName" : "Operating Systems" 
                |    |  "code" : "CSE2005" 
                |    |  "type" : "Embedded Theory",
                |    |  "subjectID" : "AP2023241000001" // Subject ID
                |    |  "updatedOn" : "Wed Apr 15 04:27:10 2020"  // Time at which attendance was fetched
                |    }
                }
        valid: bool
            True if the attendance is valid, else False.

    """

    # TODO implement a semID implementation.
    valid = False
    attendance = {}
    for semID in set(SEM_IDS):
        payload = get_attendance_payload(username, semID)
        attendance, valid = await _get_attendance_from_payload(sess, payload, username)
        if valid:
            break

    return (attendance, valid)

async def get_single_subject_attendance(sess: aiohttp.ClientSession, 
        username: str, 
        subjectID: Union[str, None], 
        slotName: str) -> List[Dict[str, str]]:
    """
        Returns the attendance of the user in the form of a dictionary.
        The dictionary is of the form 

        Parameters:
        -----------
        sess: aiohttp.ClientSession
            The session object to be used for making the request.
        username: str
            The username of the user whose attendance is to be fetched.
        subjectID: str
            The subject ID of the user whose attendance is to be fetched.

        Returns:
        -------
        [
            {
                "Attendance Date":"23-May-2023",
                "Attendance Slot":"B1",
                "Day And Timing":"TUE,09:00-09:50",
                "Attendance Status":"Present"
            },
        ]

    """
    if subjectID is None: return []
    attd_payload = generate_payload_attendance_for_subject(subjectID, slotName, username)
    async with sess.post(VTOP_SINGLE_SUBJECT_ATTENDANCE_URL, data=attd_payload, headers=HEADERS) as resp:
        return parse_single_subject_attendance(await resp.text())
