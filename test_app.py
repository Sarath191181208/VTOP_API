import aiohttp

from src.utils import print_json
from src.vtop_handler.academic_calender_handler import get_academic_calender
from src.vtop_handler.faculty_handler import get_faculty_details

from src.vtop_handler.session_generator import generate_session
from src.vtop_handler.student_academic_history import get_acadhistory
from src.vtop_handler.student_attendance import get_attendance
from src.vtop_handler.student_profile import get_student_profile
from src.vtop_handler.student_timetable import get_timetable

import os
import dotenv
dotenv.load_dotenv()

username = os.getenv('VTOP_USERNAME', "")
password = os.getenv('VTOP_PASSWORD', "")

async def get_all_details(sess: aiohttp.ClientSession, user_name: str):
    tasks = [
        get_student_profile(sess, user_name),
        get_timetable(sess, user_name),
        get_attendance(sess, user_name),
        get_acadhistory(sess, user_name),
    ]

    profile_future, timetable_future, attendance_future, academic_history_future = await asyncio.gather(*tasks)

    return {
        "profile": profile_future[0],
        "timetable": timetable_future[0],
        "attendance": attendance_future[0],
        "academic_history": academic_history_future[0]
    }

async def main():
    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(username, password, sess)
        if user_name is None: print("Login Failed!"); return
        all_details = await get_all_details(sess, user_name)
        print_json(all_details)
        print("###"*30)

        fac_details = await get_faculty_details()
        print_json(fac_details[:5])
        print("###"*30)

        acad_calender = await get_academic_calender()
        print_json(acad_calender)
        print("###"*30)

if __name__ == '__main__':
    import asyncio
    import time
    start_time = time.time()
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
