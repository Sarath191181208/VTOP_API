
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

from dotenv import load_dotenv
load_dotenv()

PORT = 5000
app = Flask(__name__)

import logging
from src.utils import c_print
logging.basicConfig(filename='flask_logs.log', level=logging.DEBUG)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/v1/alldetails', methods=['POST'])
async def all_details():
    if request.method == 'POST':

        user_name = request.form.get('username', None)
        passwd = request.form.get('password', None)
        status_code = 200

        if not is_valid_username_password(user_name, passwd):
            data = jsonify({'error': 'username or password is invalid'})
            status_code = 400
            return data, status_code

        profile, timetable, attendance, academic_history = {}, {}, {}, {}
        async with aiohttp.ClientSession() as sess:
            user_name, valid = await generate_session(user_name,passwd, sess)
            if not valid:
                status_code = 401
                data = jsonify({'error': 'invalid username or password'})
                return data, status_code
            profile_future =  get_student_profile(sess, user_name)
            timetable_future =  get_timetable(sess, user_name)
            attendance_future =  get_attendance(sess, user_name)
            academic_history_future =  get_acadhistory(sess, user_name)
            
            profile, valid = await profile_future
            timetable, valid = await timetable_future
            attendance, valid = await attendance_future
            academic_history, valid = await academic_history_future
        return jsonify({
            'profile': profile,
            'timetable': timetable,
            'attendance': attendance,
            'academic_history':academic_history
        }), status_code
    
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

    
