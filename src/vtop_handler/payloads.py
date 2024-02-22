"""

    payloads for different requests

"""
from .utils import get_curr_time_vtop_format


def get_profile_payload(user_name: str, csrf_token: str):
    return {
        "verifyMenu": "true",
        "_csrf": csrf_token,
        "authorizedID": user_name,
        "nocache": "@(new Date().getTime())"}


def get_timetable_payload(username: str,
                          semID: str, csrf_token: str):
    return {"semesterSubId": semID,
            "authorizedID": username,
            "_csrf": csrf_token,
            "x": get_curr_time_vtop_format()}


def get_attendance_payload(username: str,
                           semId: str, csrf_token: str):
    return {"semesterSubId": semId,
            "authorizedID": username,
            "_csrf": csrf_token,
            "x": get_curr_time_vtop_format()}


def get_academic_profile_payload(username: str, csrf_token: str):
    return {"verifyMenu": "true",
            "authorizedID": username,
            "_csrf": csrf_token,
            "nocache": "@(new Date().getTime())"}


def get_exam_schedule_payload(username,
                              semId, crsf_token: str):
    return {"semesterSubId": semId,
            "authorizedID": username, "_csrf": crsf_token}


def get_course_page_semeseter_names_payload(auth_id):
    return {"verifyMenu": True,
            "winImage": None,
            "authorizedID": auth_id,
            "nocache": "@(new Date().getTime())"}


def get_course_page_subject_names_payload(sub_sem_id,
                                          auth_id):
    return {"paramReturnId": "getCourseForCoursePage",
            "semSubId": sub_sem_id,
            "authorizedID": auth_id,
            "x": get_curr_time_vtop_format()}


def get_course_page_table_of_contents_payload(class_id,
                                              sem_id,
                                              auth_id):
    return {"classId": class_id,
            "praType": "source",
            "paramReturnId": "getSlotIdForCoursePage",
            "semSubId": sem_id,
            "authorizedID": auth_id,
            "x": get_curr_time_vtop_format()}


def get_download_links_payload(payload_details_dict):
    payload_details_dict.update({
        "x": get_curr_time_vtop_format()
    })
    return payload_details_dict


def get_marks_view_payload(sem_id: str,
                           auth_id: str):
    return {
        "authorizedID": auth_id,

        "semesterSubId": sem_id
    }


def get_my_curriculum_payload(roll_no: str):
    return {
        "verifyMenu": "true",
        "winImage": "undefined",
        "authorizedID": roll_no,
        "nocache": "@ (new Date().getTime())"
    }

def generate_payload_attendance_for_subject(sem_sub_id: str, course_id: str, course_type: str, auth_id: str, crsf_token: str):
    return {
        "_csrf": crsf_token,
        "semesterSubId": sem_sub_id,
        "registerNumber": auth_id,
        "courseId": course_id,
        "courseType": course_type,
        "authorizedID": auth_id,
        "x": get_curr_time_vtop_format()
    }
