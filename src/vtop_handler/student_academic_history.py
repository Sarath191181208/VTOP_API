"""
    Gives Academic History of Student or Grade History

    Usage:
    ------
    > from vtop_handler.session_generator import get_valid_session
    > from vtop_handler.student_academic_history import get_acadhistory
    > 
    > async def main():
    >   async with aiohttp.ClientSession() as sess:
    >       user_name, valid = await get_valid_session(user_name,password, sess)
    >
    >      if valid:
    >          acad_history, valid = await get_acadhistory(sess, user_name)
    >          print(acad_history)
    >
    > asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    > asyncio.run(main())
"""

import asyncio
import aiohttp

from .payloads import get_academic_profile_payload
from .constants import VTOP_ACADHISTORY_URL, HEADERS
from .parsers import parse_acadhistory

async def _get_acadhistory_from_payload(sess:aiohttp.ClientSession, payload:dict):
    valid = False
    grades = dict()
    async with sess.post(VTOP_ACADHISTORY_URL, data=payload, headers=HEADERS) as resp:
        acad_html = await resp.text()
        if resp.status == 200:
            try:
                grades = parse_acadhistory(acad_html)
                valid = True
            except Exception as e:
                print("Error in getting acad history with payload: ", payload)
                print("Falied at parsing acad history with error: ", e)
        else:
            print(f"Error in getting acad history response {resp.status} with payload: ", payload)
    return (grades, valid)

async def get_acadhistory(sess:aiohttp.ClientSession, id:str):
    """
        Returns the academic history of the user in the form of a dictionary.

        Parameters:
        -----------
        sess: aiohttp.ClientSession
            The session to be used for the request.
        id: str
            The id of the user.

        Returns:
        --------
        acad_history: dict
            The academic history of the user.
            it is of the form : {
                subjects : {
                    subjectName : grade
                    ...
                },
                summary:{
                    "CreditsRegistered" : Num,
                    "CreditsEarned" : Num,
                    "CGPA" : str,
                    "S" : Num
                    "A" : Num,
                    ...
                }
            }
        valid: bool
            True if the request was successful.
    """
    payload = get_academic_profile_payload(id)
    grades, valid = await _get_acadhistory_from_payload(sess, payload)

    return (grades, valid)
