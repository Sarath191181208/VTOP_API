import logging
from typing import Dict, Tuple

from flask import Flask, Response, jsonify, make_response, request, session
from flask_session import Session
from flask_cors import CORS
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
    get_course_page,
    get_course_page_links_payload,
    get_course_semesters_list,
    get_download_links_from_course_page,
)
from src.vtop_handler import get_timetable, get_attendance, get_acadhistory
from src.vtop_handler import get_academic_calender, get_faculty_details
from src.vtop_handler import generate_session, get_student_profile
from src.vtop_handler.marks_view import get_marks_dict
from src.vtop_handler.curriculum import get_curriculum_info
from src.const import (
    CORS_RESOURCE_LIST,
    IS_VIT_AP_SERVER_DOWN,
    PARTIAL_CONTENT_STATUS_CODE,
    SAMPLE_RESPONSE,
    SUCCESS_STATUS_CODE,
    UNAUTHORIZED_STATUS_CODE,
)


PORT = 5000
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 15 * 60
app.config["SESSION_TYPE"] = "filesystem"
cors = CORS(app, resources=CORS_RESOURCE_LIST)
Session(app)

logging.basicConfig(filename="flask_logs.log", level=logging.DEBUG)


def get_all_details_futures(sess: aiohttp.ClientSession, user_name: str, csrf_token: str):
    profile_future = get_student_profile(sess, user_name, csrf_token)
    timetable_future = get_timetable(sess, user_name, csrf_token)
    attendance_future = get_attendance(sess, user_name, csrf_token )
    academic_history_future = get_acadhistory(sess, user_name, csrf_token)

    return {
        "profile": profile_future,
        "timetable": timetable_future,
        "attendance": attendance_future,
        "academic_history": academic_history_future,
    }


def get_cookies(sess_cookie: str) -> Dict[str, str]:
    return {
        "JSESSIONID": sess_cookie,  # type: ignore
        "loginUserType": "vtopuser",
    }

@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/api/v1/alldetails", methods=["POST"])
@may_throw
async def all_details():
    user_name = request.form.get("username", None)
    passwd = request.form.get("password", None)
    throw_if_invalid_username_password(user_name, passwd)

    if user_name is None or passwd is None:
        raise BadRequestException("You must provide username and password to access this route!")

    if IS_VIT_AP_SERVER_DOWN:
        return jsonify(SAMPLE_RESPONSE), PARTIAL_CONTENT_STATUS_CODE

    async with aiohttp.ClientSession() as sess:
        user_name, csrf_token = await generate_session(user_name, passwd, sess)
        if user_name is None:
            raise InvalidCredentialsException(status_code=UNAUTHORIZED_STATUS_CODE)
        all_details_futures = get_all_details_futures(sess, user_name, csrf_token)
        # awaiting all details to arrive and converting to dict
        all_detials = {
            k: (await d_future)[0] for k, d_future in all_details_futures.items()
        }
    # return jsonify(all_detials, ), 200
    response = make_response(jsonify(all_detials), SUCCESS_STATUS_CODE)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/api/v1/exam_schedule", methods=["POST"])
async def exam_schedule():
    user_name = request.form.get("username", "")
    passwd = request.form.get("password", "")

    throw_if_invalid_username_password(user_name, passwd)

    async with aiohttp.ClientSession() as sess:
        user_name, crsf_token = await generate_session(user_name, passwd, sess)
        if user_name is None:
            raise InvalidCredentialsException(status_code=UNAUTHORIZED_STATUS_CODE)
        all_detials, _ = await get_exam_schedule(sess, user_name, crsf_token)

    return jsonify(all_detials), 200


@app.route("/api/v1/login", methods=["POST"])
@may_throw
async def login():
    if "cookie" in session:
        return jsonify({"cookie": session.get("cookie")}), 200

    cookie = None
    user_name = request.form.get("username", "")
    passwd = request.form.get("password", "")

    throw_if_invalid_username_password(user_name, passwd)
    # extract cookie from vtop
    async with aiohttp.ClientSession() as sess:
        user_name, crsf_token = await generate_session(user_name, passwd, sess)
        cookie = (
            sess.cookie_jar.filter_cookies("https://vtop2.vitap.ac.in/vtop")
            .get("JSESSIONID")
            .value
        )  # type: ignore
        if user_name is None:
            raise InvalidCredentialsException(status_code=UNAUTHORIZED_STATUS_CODE)

    session["cookie"] = cookie
    session["auth_id"] = user_name
    session["crsf_token"] = crsf_token

    response = make_response(jsonify({"cookie": cookie}), SUCCESS_STATUS_CODE)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/api/v1/clear_cookies", methods=["POST"])
async def clear_coookies():
    if "cookie" in session:
        session.pop("cookie")
        session.pop("auth_id")
        session.pop("crsf_token")
    return jsonify(None)


@app.route("/api/v1/get_semester_names_codes", methods=["POST"])
@is_logged_in
@may_throw
async def get_semester_names_codes():
    raise_if_not_args_passed(request.form, "auth_id")
    auth_id = request.form["auth_id"]
    crsf_token = request.form.get("csrf_token", session.get("crsf_token"))
    if crsf_token is None:
        raise BadRequestException("You must provide csrf_token to access this route!")
    cookies = {"JSESSIONID": session.get("cookie"), "loginUserType": "vtopuser"}
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        semester_names_codes_dict = await get_course_semesters_list(sess, auth_id, crsf_token)

    return jsonify(semester_names_codes_dict), 200


@app.route("/api/v1/get_course_details", methods=["POST"])
@is_logged_in
@may_throw
async def get_course_details():
    course_details = {}
    raise_if_not_args_passed(request.form, "auth_id", "semester_name_code")
    auth_id = request.form["auth_id"]
    semester_name_code = request.form["semester_name_code"]

    cookies = {"JSESSIONID": session.get("cookie"), "loginUserType": "vtopuser"}
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        course_details = await get_course_page(sess, auth_id, semester_name_code)
    return jsonify(course_details), 200


@app.route("/api/v1/get_course_page_entries_link_payloads", methods=["POST"])
@is_logged_in
@may_throw
async def get_course_page_entries_link_payloads():
    raise_if_not_args_passed(request.form, "class_id", "sem_id", "auth_id")
    class_id = request.form["class_id"]
    sem_id = request.form["sem_id"]
    auth_id = request.form["auth_id"]

    cookies = {"JSESSIONID": session.get("cookie"), "loginUserType": "vtopuser"}
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        links_payloads_list = await get_course_page_links_payload(
            sess, class_id, sem_id, auth_id
        )
    return jsonify(links_payloads_list), 200


@app.route("/api/v1/get_download_links", methods=["POST"])
@is_logged_in
@may_throw
async def get_download_links():
    json_data = request.get_json()
    if json_data is None:
        raise BadRequestException("You must provide json data to access this route!")
    json_data.update({"authorizedID": session.get("auth_id")})
    cookies = {"JSESSIONID": session.get("cookie"), "loginUserType": "vtopuser"}
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        download_links = await get_download_links_from_course_page(sess, json_data)
    return jsonify(download_links), 200


@app.route("/api/v1/fetch_marks", methods=["POST"])
@is_logged_in
@may_throw
async def fetch_marks():
    raise_if_not_args_passed(request.form, "sem_id", "roll_no")
    sem_id = request.form["sem_id"]
    roll_no = request.form["roll_no"]

    cookies = get_cookies(session.get("cookie"))
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        marks_dict = await get_marks_dict(sess, roll_no, sem_id)
    return jsonify(marks_dict), 200

@app.route("/api/v2/get_curriculum", methods=["POST"])
@may_throw
async def get_curriculum2() -> Tuple[Response, int]:
    raise_if_not_args_passed(request.form, "roll_no", "cookie", "csrf_token")
    auth_id = request.form["roll_no"]
    cookie = request.form["cookie"]
    token = request.form["csrf_token"]
    cookies = get_cookies(cookie)
    async with aiohttp.ClientSession(cookies=cookies) as sess:
        curriculum = await get_curriculum_info(sess, auth_id, token)
    response = make_response(jsonify(curriculum.dict()), SUCCESS_STATUS_CODE)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response, SUCCESS_STATUS_CODE


@app.route("/api/v1/faculty", methods=["POST"])
async def faculty():
    res = await get_faculty_details()
    return jsonify(res)


@app.route("/api/v1/academic_calenders", methods=["POST"])
async def acad_calenders():
    res = await get_academic_calender()
    return jsonify(res)


if __name__ == "__main__":
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(app.run(debug=True, port=PORT))
    app.run(debug=True, port=PORT)
    # app.host(host='0.0.0.0', port=PORT)
