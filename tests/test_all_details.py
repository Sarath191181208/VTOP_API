import asyncio
import os
import aiohttp
import pytest
from vtop_handler import (
    generate_session,
    get_acadhistory,
    get_attendance,
    get_student_profile,
    get_timetable)

import dotenv
dotenv.load_dotenv()

USERNAME = os.getenv('VTOP_USERNAME_1', None)
PASSWORD = os.getenv('VTOP_PASSWORD_1', None)
VITEEE_USERNAME_1 = os.getenv('VITEEE_USERNAME_1', None)
VITEEE_PASSWORD_1 = os.getenv('VITEEE_PASSWORD_1', None)
FRESHER_USERNAME_1 = os.getenv('FRESHER_USERNAME_1', None)
FRESHER_PASSWORD_1 = os.getenv('FRESHER_PASSWORD_1', None)

for i in [USERNAME, PASSWORD,
          VITEEE_USERNAME_1, VITEEE_PASSWORD_1,
          FRESHER_USERNAME_1, FRESHER_PASSWORD_1]:
    assert i is not None, "Please set the environment variables"


async def get_all_details(sess: aiohttp.ClientSession, user_name: str):
    tasks = [
        get_student_profile(sess, user_name),
        get_timetable(sess, user_name),
        get_attendance(sess, user_name),
        get_acadhistory(sess, user_name),
    ]

    (profile_future,
     timetable_future,
     attendance_future,
     academic_history_future) = await asyncio.gather(*tasks)

    return {
        "profile": profile_future[0],
        "timetable": timetable_future[0],
        "attendance": attendance_future[0],
        "academic_history": academic_history_future[0]
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("username, password", [
    (USERNAME, PASSWORD),
    (VITEEE_USERNAME_1, VITEEE_PASSWORD_1),
    (FRESHER_USERNAME_1, FRESHER_PASSWORD_1)
])
async def test_all_details(username, password):
    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(username, password, sess)
        if user_name is None:
            assert False, "Login Failed!"
        all_details = await get_all_details(sess, user_name)

        for k, v in all_details.items():
            assert v is not None, f"Failed to get {k}"
