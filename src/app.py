
from flask import Flask, jsonify, request

import asyncio
import aiohttp
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.vtop_handler import generate_session, get_student_profile
from src.vtop_handler import get_timetable, get_attendance, get_acadhistory
from src.vtop_handler import get_academic_calender, get_faculty_details

from src.validators import is_valid_username_password
from src.custom_exceptions import InvalidCredentialsException

from dotenv import load_dotenv
load_dotenv()

PORT = 5000
app = Flask(__name__)

import logging
from src.utils import c_print
logging.basicConfig(filename='flask_logs.log', level=logging.DEBUG)

def get_all_details_futures(sess: aiohttp.ClientSession, user_name: str):
    profile_future =  get_student_profile(sess, user_name)
    timetable_future =  get_timetable(sess, user_name)
    attendance_future =  get_attendance(sess, user_name)
    academic_history_future =  get_acadhistory(sess, user_name)

    return {
        "profile": profile_future,
        "timetable": timetable_future,
        "attendance": attendance_future,
        "academic_history": academic_history_future
    }

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/v1/alldetails', methods=['POST'])
async def all_details():
    if request.method == 'POST':
        try: 
            user_name = request.form.get('username', None)
            passwd = request.form.get('password', None)

            if not is_valid_username_password(user_name, passwd):
                raise InvalidCredentialsException(status_code=400)

            async with aiohttp.ClientSession() as sess:
                user_name, valid = await generate_session(user_name,passwd, sess)
                if not valid:
                    raise InvalidCredentialsException(status_code=401)
                all_details_futures = get_all_details_futures(sess, user_name)
                # awaiting all details to arrive and converting to dict
                all_detials = {
                    k: (await d_future)[0]
                    for k, d_future in all_details_futures.items()
                }
        except InvalidCredentialsException as ICexception:
            return jsonify({"Error": ICexception.msg}), ICexception.status_code

        status_code = 200
        return jsonify(all_detials), status_code
    
@app.route('/api/v1/faculty', methods=['POST'])
async def faculty():
    res = await get_faculty_details()
    return jsonify(res)

@app.route('/api/v1/academic_calenders', methods=['POST'])
async def acad_calenders():
    res = await get_academic_calender()
    return jsonify(res)

if __name__ == "__main__":
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(app.run(debug=True, port=PORT))
    app.run(debug=True, port=PORT)
    # app.host(host='0.0.0.0', port=PORT)

    
