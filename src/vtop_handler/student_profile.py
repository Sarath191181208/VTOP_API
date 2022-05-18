"""
    Gets the student profile using a session and returns a dictionary of the profile

    Usage:
    ------
    > from vtop_handler.session_generator import get_valid_session
    > from vtop_handler.student_profile import get_student_profile
    > 
    > async def main():
    >   async with aiohttp.ClientSession() as sess:
    >       user_name, valid = await get_valid_session(user_name,password, sess)
    >
    >      if valid:
    >          profile, valid = await get_student_profile(sess, user_name)
    >          print(profile)
    >
    > asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    > asyncio.run(main())
"""
import aiohttp
import asyncio

from typing import Tuple

from .payloads import get_vtop_profile_payload
from .constants import HEADERS, VTOP_PROFILE_URL
from .parsers import parse_profile

async def get_student_profile(sess: aiohttp.ClientSession, username: str)->Tuple[dict, bool]:
    """
    Returns Students Personal Details in the form of a dict 

    Parameters
    ----------
    sess: aiohttp.ClientSession
        Session object
    username: str
        Username of the student

    Returns
    -------
    profile: dict
        Dictionary of the student profile
        {
            |  "name: "Name of the student",
            |  "branch": "Cmoputer Science",
            |  "program" : "BTECH",
            |  "regno" : "21BCE0123",
            |  "appNo" : "983y40983",
            |  "school" : "School of sjdhjs oshdvojs",
            |  "email" : "notgonnatypehere@gmail.com",
            |  "proctorEmail" : "yeahkillhim@yahoo.com",
            |  "proctorName' "Good Guy",
        }
    valid: bool
        True if the profile is valid
    """
    valid = False
    profile = dict()
    payload = get_vtop_profile_payload(username)
    async with sess.post(VTOP_PROFILE_URL, data=payload, headers = HEADERS) as resp:
        profile_html = await resp.text()
        if resp.status == 200: # i.e we get the profile data
            try:
                profile = parse_profile(profile_html)
                valid = True
            except Exception as e:
                print("parsing profile failed with error: ", e)

    return (profile, valid)
