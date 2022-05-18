
from flask import Flask, jsonify, request, Response

import asyncio
import aiohttp

from vtop_handler import get_valid_session, get_student_profile
from vtop_handler import get_timetable, get_attendance, get_acadhistory

import os
from dotenv import load_dotenv
load_dotenv()

PORT = 5000
app = Flask(__name__)

import logging
from utils import c_print
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

        if user_name is None or passwd is None:
            data = jsonify({'error': 'username or password is empty'})
            status_code = 400
            return Response(data, status=status_code, mimetype='application/json')

        profile, timetable, attendance, academic_history = {}, {}, {}, {}
        try:
            async with aiohttp.ClientSession() as sess:
                user_name, valid = await get_valid_session(user_name,passwd, sess)
                if valid:
                    profile, valid = await get_student_profile(sess, user_name)
                    timetable, valid = await get_timetable(sess, user_name)
                    attendance, valid = await get_attendance(sess, user_name)
                    academic_history, valid = await get_acadhistory(sess, user_name)
                else:
                    status_code = 401
                    data = jsonify({'error': 'invalid username or password'})
                    return Response(data, status=status_code, mimetype='application/json')
        except Exception as e:
            status_code = 500
            print(e, e.with_traceback())
            logging.warning(e)
        finally:
            return Response(jsonify({
                'profile': profile,
                'timetable': timetable,
                'attendance': attendance,
                'academic_history':academic_history
            }), status=status_code, mimetype='application/json')
        

if __name__ == "__main__":
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(app.run(debug=True, port=PORT))
    app.run(debug=True, port=PORT)

    
