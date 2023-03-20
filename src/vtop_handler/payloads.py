"""

    payloads for different requests

"""
from .utils import get_curr_time_vtop_format


def get_profile_payload(user_name):
    return {
        "verifyMenu": "true",
        "winImage": "undefined",
        "authorizedID": user_name,
        "nocache": "@(new Date().getTime())"}


def get_timetable_payload(username,
                          semID):
    return {"semesterSubId": semID,
            "authorizedID": username,
            "x": get_curr_time_vtop_format()}


def get_attendance_payload(username,
                           semId):
    return {"semesterSubId": semId,
            "authorizedID": username,
            "x": get_curr_time_vtop_format()}


def get_academic_profile_payload(username):
    return {"verifyMenu": "true",
            "winImage": "undefined",
            "authorizedID": username,
            "nocache": "@(new Date().getTime())"}


def get_exam_schedule_payload(username,
                              semId):
    return {"semesterSubId": semId,
            "authorizedID": username}


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
