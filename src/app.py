from src.vtop_handler.marks_view import get_marks_dict
from src.vtop_handler.curriculum import get_curriculum_info
import logging
from typing import Dict, Tuple
from flask import Flask, Response, jsonify, request, session
from flask_session import Session
import aiohttp
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.decorators import is_logged_in, may_throw, raise_if_not_args_passed
from src.vtop_handler.Exceptions import InvalidCredentialsException, BadRequestException
from src.validators import throw_if_invalid_username_password
from src.vtop_handler import get_exam_schedule
from src.vtop_handler.course_page_handler import (
    get_course_page, get_course_page_links_payload, 
    get_course_semesters_list, 
    get_download_links_from_course_page)
from src.vtop_handler import get_timetable, get_attendance, get_acadhistory
from src.vtop_handler import get_academic_calender, get_faculty_details
from src.vtop_handler import generate_session, get_student_profile



PORT = 5000
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 15 * 60
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

logging.basicConfig(filename='flask_logs.log', level=logging.DEBUG)


def get_all_details_futures(sess: aiohttp.ClientSession, user_name: str):
    profile_future = get_student_profile(sess, user_name)
    timetable_future = get_timetable(sess, user_name)
    attendance_future = get_attendance(sess, user_name)
    academic_history_future = get_acadhistory(sess, user_name)

    return {
        "profile": profile_future,
        "timetable": timetable_future,
        "attendance": attendance_future,
        "academic_history": academic_history_future
    }


def get_cookies() -> Dict[str, str]:
    return {
        'JSESSIONID': session.get("cookie"),  # type: ignore
        "loginUserType": "vtopuser"
    }


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/v1/alldetails', methods=['POST'])
@may_throw
async def all_details():

    user_name = request.form.get('username', "")
    passwd = request.form.get('password', "")

    throw_if_invalid_username_password(user_name, passwd)

    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(user_name, passwd, sess)
        if user_name is None:
            raise InvalidCredentialsException(status_code=401)
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

    throw_if_invalid_username_password(user_name, passwd)

    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(user_name, passwd, sess)
        if user_name is None:
            raise InvalidCredentialsException(status_code=401)
        all_detials, is_valid = await get_exam_schedule(sess, user_name)

    return jsonify(all_detials), 200


@app.route('/api/v1/login', methods=['POST'])
@may_throw
async def login():
    if "cookie" in session:
        return jsonify({"cookie": session.get("cookie")}), 200

    cookie = None
    user_name = request.form.get('username', "")
    passwd = request.form.get('password', "")

    throw_if_invalid_username_password(user_name, passwd)
    # extract cookie from vtop
    async with aiohttp.ClientSession() as sess:
        user_name = await generate_session(user_name, passwd, sess)
        cookie = sess.cookie_jar.filter_cookies(
            'https://vtop2.vitap.ac.in/vtop').get('JSESSIONID').value  # type: ignore
        if user_name is None:
            raise InvalidCredentialsException(status_code=401)

    session["cookie"] = cookie
    session["auth_id"] = user_name
    return jsonify({"cookie": cookie}), 200


@app.route('/api/v1/clear_cookies', methods=['POST'])
async def clear_coookies():
    if "cookie" in session:
        session.pop('cookie')
        session.pop('auth_id')


@app.route('/api/v1/get_semester_names_codes', methods=['POST'])
@is_logged_in
@may_throw
async def get_semester_names_codes():
    raise_if_not_args_passed(request.form, 'auth_id')
    auth_id = request.form['auth_id']
    cookies = {
        'JSESSIONID': session.get("cookie"),
        "loginUserType": "vtopuser"
    }
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        semester_names_codes_dict = await get_course_semesters_list(sess, auth_id)

    return jsonify(semester_names_codes_dict), 200


@app.route('/api/v1/get_course_details', methods=['POST'])
@is_logged_in
@may_throw
async def get_course_details():
    course_details = {}
    raise_if_not_args_passed(request.form, 'auth_id', 'semester_name_code')
    auth_id = request.form['auth_id']
    semester_name_code = request.form['semester_name_code']

    cookies = {
        'JSESSIONID': session.get("cookie"),
        "loginUserType": "vtopuser"
    }
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        course_details = await get_course_page(sess, auth_id, semester_name_code)
    return jsonify(course_details), 200


@app.route('/api/v1/get_course_page_entries_link_payloads', methods=['POST'])
@is_logged_in
@may_throw
async def get_course_page_entries_link_payloads():
    raise_if_not_args_passed(request.form, 'class_id', 'sem_id', 'auth_id')
    class_id = request.form['class_id']
    sem_id = request.form['sem_id']
    auth_id = request.form['auth_id']

    cookies = {
        'JSESSIONID': session.get("cookie"),
        "loginUserType": "vtopuser"
    }
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        links_payloads_list = await get_course_page_links_payload(
            sess, class_id, sem_id, auth_id)
    return jsonify(links_payloads_list), 200


@app.route('/api/v1/get_download_links', methods=['POST'])
@is_logged_in
@may_throw
async def get_download_links():
    json_data = request.get_json()
    if json_data is None:
        raise BadRequestException(
            "You must provide json data to access this route!")
    json_data.update({"authorizedID": session.get("auth_id")})
    cookies = {
        'JSESSIONID': session.get("cookie"),
        "loginUserType": "vtopuser"
    }
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        download_links = await get_download_links_from_course_page(sess, json_data)
    return jsonify(download_links), 200


@app.route("/api/v1/fetch_marks", methods=["POST"])
@is_logged_in
@may_throw
async def fetch_marks():
    raise_if_not_args_passed(request.form, 'sem_id', 'auth_id')
    sem_id = request.form['sem_id']
    auth_id = request.form['auth_id']

    cookies = get_cookies()
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        marks_dict = await get_marks_dict(sess, auth_id, sem_id)
    return jsonify(marks_dict), 200


@app.route("/download_")
# @app.route('/download_class_materials', methods=["GET"])
# @may_throw
# @is_cookie_present
# async def download_class_materials():
#     raise_if_not_args_passed(request.args, "download_suffix", "auth_id")
#     download_suffix = request.args.get("download_suffix")
#     auth_id = request.args.get("auth_id")
#     download_link = f"https://vtop2.vitap.ac.in/vtop/{download_suffix}?authorizedID={auth_id}&x={get_curr_time_vtop_format()}"
#     cookies = {
#         'JSESSIONID': session.get("cookie"),
#         "loginUserType": "vtopuser"
#     }
#     async with aiohttp.ClientSession(cookies=cookies) as sess:
#         async with sess.get(download_link) as resp:
#             if resp.status != 200:
#                 print(resp.status)
#                 raise BadRequestException(
#                     "Something went wrong while downloading the file!")
#             file_name = (resp.headers.get("Content-Disposition", "")
#                          .split("filename=")[1]
#                          .replace('"', ''))
#             return send_file(BytesIO(await resp.read()), attachment_filename=file_name, as_attachment=True, download_name=file_name)
# return await resp.read(), 200, {"Content-Disposition": f"attachment; filename={file_name}"}

@app.route('/api/v1/get_curriculum', methods=['POST'])
@is_logged_in
@may_throw
async def get_curriculum() -> Tuple[Response, int]:
    raise_if_not_args_passed(request.form, 'roll_no')
    auth_id = request.form['roll_no']
    cookies = get_cookies()
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        curriculum = await get_curriculum_info(sess, auth_id)
    return jsonify(curriculum.dict()), 200

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
