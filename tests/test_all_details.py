import asyncio
import aiohttp
import pytest
from vtop_handler import (
    generate_session,
    get_acadhistory,
    get_attendance,
    get_student_profile,
    get_timetable)

from user_names_passwords import username_password_list

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
@pytest.mark.parametrize("username, password", username_password_list)
async def test_all_details(username, password):
    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(username, password, sess)
        if user_name is None:
            assert False, "Login Failed!"
        all_details = await get_all_details(sess, user_name)

        for k, v in all_details.items():
            assert v is not None or len(v) == 0 , f"Failed to get {k}"
