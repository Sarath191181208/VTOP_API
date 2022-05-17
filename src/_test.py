import aiohttp
import asyncio

from vtop_handler import get_valid_session, get_student_profile
from vtop_handler import  get_timetable, get_attendance, get_acadhistory

async def main():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    user_name = os.getenv('VTOP_USERNAME')
    passwd = os.getenv('VTOP_PASSWORD')

    async with aiohttp.ClientSession() as sess:
        user_name, valid = await get_valid_session(user_name,passwd, sess)
        if valid:
            profile, valid = await get_student_profile(sess, user_name)
            timetable, valid = await get_timetable(sess, user_name)
            attendance, valid = await get_attendance(sess, user_name)
            academic_history, valid = await get_acadhistory(sess, user_name)

            print(profile)
            print(timetable)
            print(attendance)
            print(academic_history)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
# res, status = get_student_profile(sess, username)
# get_acadhistory(sess, username)
# print(res)
