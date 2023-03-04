from flask import Flask, jsonify, request, session
from flask_session import Session
import asyncio
import aiohttp
import sys
import os

from src.vtop_handler.parsers.parse_course_page import parse_to_get_view_urls

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.vtop_handler import generate_session, get_student_profile
from src.vtop_handler import get_academic_calender, get_faculty_details
from src.vtop_handler import get_timetable, get_attendance, get_acadhistory
from src.vtop_handler.course_page_handler import get_course_page, get_course_page_links_payload, get_course_semesters_list
from src.vtop_handler import get_exam_schedule

from src.validators import validate_username_password

from src.vtop_handler.Exceptions import CustomBaseException, InvalidCredentialsException, BadRequestException

from src.decorators import is_cookie_present, may_throw

PORT = 5000
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 15 * 60
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

import logging
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
@may_throw
async def all_details():

    user_name = request.form.get('username', "")
    passwd = request.form.get('password', "")

    validate_username_password(user_name, passwd)

    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(user_name,passwd, sess)
        if user_name is None: raise InvalidCredentialsException(status_code=401)
        all_details_futures = get_all_details_futures(sess, user_name)
        # awaiting all details to arrive and converting to dict
        all_detials = {
            k: (await d_future)[0]
            for k, d_future in all_details_futures.items()
        }
    return jsonify(all_detials), 200
    
@app.route('/api/v1/exam_schedule', methods=['POST'])
async def exam_schedule():
    user_name = request.form.get('username', "")
    passwd = request.form.get('password', "")

    validate_username_password(user_name, passwd)

    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(user_name,passwd, sess)
        if user_name is None: raise InvalidCredentialsException(status_code=401)
        all_detials, is_valid = await get_exam_schedule(sess, user_name)

    return jsonify(all_detials), 200

@app.route('/api/v1/login', methods=['POST'])
@may_throw
async def login():
    cookie = None
    user_name = request.form.get('username', "")
    passwd = request.form.get('password', "")

    validate_username_password(user_name, passwd)
    # extract cookie from vtop
    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(user_name,passwd, sess)
        cookie = sess.cookie_jar.filter_cookies('https://vtop2.vitap.ac.in/vtop').get('JSESSIONID').value # type: ignore
        if user_name is None: raise InvalidCredentialsException(status_code=401)
    
    session["cookie"] = cookie
    return jsonify({"cookie": cookie}), 200

@app.route('/api/v1/get_semester_names_codes', methods=['POST'])
@is_cookie_present
@may_throw
async def get_semester_names_codes():
    auth_id = request.form.get('auth_id', None)
    if auth_id is None: raise BadRequestException("You must provide auth_id to access this route!")
    cookies = {
        'JSESSIONID': session.get("cookie"),
        "loginUserType": "vtopuser"
    }
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        semester_names_codes_dict = await get_course_semesters_list(sess, auth_id)

    return jsonify(semester_names_codes_dict), 200


@app.route('/api/v1/get_course_details', methods=['POST'])
@is_cookie_present
@may_throw
async def get_course_details():
    course_details = {}
    auth_id = request.form.get('auth_id', None)
    semester_name_code = request.form.get('semester_name_code', None)

    if auth_id is None: raise BadRequestException("You must provide auth_id to access this route!")
    if semester_name_code is None: raise BadRequestException("You must provide semester_name_code to access this route!")

    cookies = {
        'JSESSIONID': session.get("cookie"),
        "loginUserType": "vtopuser"
    }
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        course_details = await get_course_page(sess, auth_id, semester_name_code)
    return jsonify(course_details), 200

@app.route('/api/v1/get_course_page_entries_link_payloads', methods=['POST'])
@is_cookie_present
@may_throw
async def get_course_page_entries_link_payloads():
    class_id = request.form.get('class_id', None)
    sem_id = request.form.get('sem_id', None)
    auth_id = request.form.get('auth_id', None)

    if class_id is None: raise BadRequestException("You must provide class_id to access this route!")
    if sem_id is None: raise BadRequestException("You must provide sem_id to access this route!")
    if auth_id is None: raise BadRequestException("You must provide auth_id to access this route!")

    cookies = {
        'JSESSIONID': session.get("cookie"),
        "loginUserType": "vtopuser"
    }
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        links_payloads_list = await get_course_page_links_payload(sess, auth_id, class_id, sem_id)
    return jsonify(links_payloads_list), 200


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

    
