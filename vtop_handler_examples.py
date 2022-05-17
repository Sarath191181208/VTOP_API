########### Generating a session  ###############

import aiohttp
import asyncio

# This is just done so that the passwords and the usernames aren't visible in the code
import os
from dotenv import load_dotenv
load_dotenv()
user_name = os.getenv('VTOP_USERNAME')
passwd = os.getenv('VTOP_PASSWORD')

async def session_example():
    from vtop_handler import get_valid_session

    async with aiohttp.ClientSession() as sess:
        user_name, valid = await get_valid_session(user_name, passwd , sess)
        print(user_name, valid)

def run_session_example():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(session_example())

########### /Generating a session  ###############
########### ---------------------  ###############
###########    Student profile     ###############

async def profile_example():
    from vtop_handler.session_generator import get_valid_session
    from vtop_handler.student_profile import get_student_profile

    async with aiohttp.ClientSession() as sess:
        user_name, valid = await get_valid_session(user_name,passwd, sess)
        print(user_name, valid)
        profile, valid = await get_student_profile(sess, user_name)
        print(profile, valid)

def run_profile_example():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(profile_example())

###########    /Student profile    ###############
########### ---------------------  ###############
###########    Student timetable    ###############

async def timetable_example():
    from vtop_handler.session_generator import get_valid_session
    from vtop_handler.student_timetable import get_timetable

    async with aiohttp.ClientSession() as sess:
        user_name, valid = await get_valid_session(user_name,passwd, sess)
        time_table, valid = await get_timetable(sess, user_name)
        print(time_table)

def run_timetable_example():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(timetable_example())

###########    /Student timetable  ###############
########### ---------------------  ###############
###########    Student attendance  ###############

async def attendance_example():
    from vtop_handler.session_generator import get_valid_session
    from vtop_handler.student_attendance import get_attendance

    import os
    from dotenv import load_dotenv
    load_dotenv()
    user_name, passwd = os.getenv('VTOP_USERNAME_2'), os.getenv('VTOP_PASSWORD_2')

    async with aiohttp.ClientSession() as sess:
        user_name, valid = await get_valid_session(user_name,passwd, sess)
        attendance, valid = await get_attendance(sess, user_name)
        print(attendance, valid)

def run_attendance_example():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(attendance_example())
###########    Student attendance  ###############
###########    ------------------  ###############
###########    Student Academic History  ###############

async def acadhistory_example():
    from vtop_handler.session_generator import get_valid_session
    from vtop_handler.student_academic_history import get_acadhistory

    async with aiohttp.ClientSession() as sess:
        user_name, valid = await get_valid_session(user_name,passwd, sess)
        if valid:
            acad_history, valid = await get_acadhistory(sess, user_name)
            print(acad_history)

def run_acadhistory_example():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(acadhistory_example())
###########    /Student Academic History  ###############


if __name__ == "__main__":
    run_session_example()
    run_profile_example()
    run_timetable_example()
    run_attendance_example()
    run_acadhistory_example()

