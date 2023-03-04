from flask import Flask, jsonify, request, session
from flask_session import Session
import asyncio
import aiohttp
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.vtop_handler import generate_session, get_student_profile
from src.vtop_handler import get_academic_calender, get_faculty_details
from src.vtop_handler import get_timetable, get_attendance, get_acadhistory
from src.vtop_handler.course_page_handler import get_course_semesters_list
from src.vtop_handler import get_exam_schedule

from src.validators import is_valid_username_password

from src.vtop_handler.Exceptions import InvalidCredentialsException, BadRequestException

from time import time

PORT = 5000
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 15 * 60
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

            if user_name is None or passwd is None or not is_valid_username_password(user_name, passwd):
                raise InvalidCredentialsException(status_code=400)

            async with aiohttp.ClientSession() as sess:
                user_name = await generate_session(user_name,passwd, sess)
                if user_name is None: raise InvalidCredentialsException(status_code=401)
                all_details_futures = get_all_details_futures(sess, user_name)
                # awaiting all details to arrive and converting to dict
                all_detials = {
                    k: (await d_future)[0]
                    for k, d_future in all_details_futures.items()
                }
        except InvalidCredentialsException as ICexception:
            return jsonify({"Error": ICexception.msg}), ICexception.status_code
        except Exception as e:
            logging.exception(e)
            return jsonify({"Error": "Internal Server Error"}), 500

        return jsonify(all_detials), 200
    
@app.route('/api/v1/exam_schedule', methods=['POST'])
async def exam_schedule():
    if request.method == 'POST':
        try: 
            user_name = request.form.get('username', None)
            passwd = request.form.get('password', None)

            if user_name is None or passwd is None or not is_valid_username_password(user_name, passwd):
                raise InvalidCredentialsException(status_code=400)

            async with aiohttp.ClientSession() as sess:
                user_name = await generate_session(user_name,passwd, sess)
                if user_name is None: raise InvalidCredentialsException(status_code=401)
                all_detials, is_valid = await get_exam_schedule(sess, user_name)

        except InvalidCredentialsException as ICexception:
            return jsonify({"Error": ICexception.msg}), ICexception.status_code
        except Exception as e:
            logging.exception(e)
            return jsonify({"Error": "Internal Server Error"}), 500

        return jsonify(all_detials), 200

@app.route('/api/v1/login', methods=['POST'])
async def login():
    cookie = None
    try: 
        user_name = request.form.get('username', None)
        passwd = request.form.get('password', None)

        if user_name is None or passwd is None or not is_valid_username_password(user_name, passwd):
            raise InvalidCredentialsException(status_code=400)
        # extract cookie from vtop
        async with aiohttp.ClientSession() as sess:
            user_name = await generate_session(user_name,passwd, sess)
            cookie = sess.cookie_jar.filter_cookies('https://vtop2.vitap.ac.in/vtop').get('JSESSIONID').value # type: ignore
            if user_name is None: raise InvalidCredentialsException(status_code=401)
    except InvalidCredentialsException as ICexception:
        return jsonify({"Error": ICexception.msg}), ICexception.status_code
    except Exception as e:
        logging.exception(e)
        return jsonify({"Error": "Internal Server Error"}), 500
    
    session["cookie"] = cookie
    return jsonify({"cookie": cookie}), 200

@app.route('/api/v1/get_semester_names_codes', methods=['POST'])
async def get_semester_names_codes():
    print(session)
    cookie = session.get("cookie", None)
    semester_names_codes_dict = {}
    if cookie is None: return jsonify({"Error": "You must login to access this route! "}), 401
    try:
        auth_id = request.form.get('auth_id', None)
        if auth_id is None: raise BadRequestException("You must provide auth_id to access this route!")
        cookies = {
            'JSESSIONID': cookie,
            "loginUserType": "vtopuser"
        }
        async with aiohttp.ClientSession(cookies=cookies) as sess:
            semester_names_codes_dict = await get_course_semesters_list(sess, auth_id)
    except BadRequestException as ICexception:
        return jsonify({"Error": ICexception.msg}), ICexception.status_code
    except Exception as e:
        logging.exception(e)
        return jsonify({"Error": "Internal Server Error"}), 500
    
    return jsonify(semester_names_codes_dict), 200

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

    
