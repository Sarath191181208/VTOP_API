"""

    payloads for different requests

"""
from .utils import get_curr_time_vtop_format

get_profile_payload = lambda user_name:{
    "verifyMenu" : "true",        
    "winImage" : "undefined",
    "authorizedID": user_name,
    "nocache" : "@(new Date().getTime())"   
}

get_timetable_payload = lambda username, semID:{
            "semesterSubId" : semID,      
            "authorizedID" : username,
            "x" : get_curr_time_vtop_format() 
}

get_attendance_payload = lambda username, semId : {
        "semesterSubId" : semId,  
        "authorizedID" : username,
        "x" : get_curr_time_vtop_format() 
}

get_academic_profile_payload = lambda username:{
        "verifyMenu" : "true",        
        "winImage" : "undefined",
        "authorizedID": username,
        "nocache" : "@(new Date().getTime())"   
}

get_exam_schedule_payload = lambda username, semId : {
        "semesterSubId" : semId,
        "authorizedID" : username,
}

get_course_page_semeseter_names_payload = lambda auth_id :  {
        "verifyMenu": True,
        "winImage": None,
        "authorizedID": auth_id,
        "nocache": "@(new Date().getTime())"
}

get_course_page_subject_names_payload = lambda sub_sem_id, auth_id: {
        "paramReturnId": "getCourseForCoursePage",
        "semSubId": sub_sem_id,
        "authorizedID": auth_id,
        "x": get_curr_time_vtop_format()
}

get_course_page_table_of_contents_payload = lambda class_id, sem_id, auth_id:{
        "classId": class_id,
        "praType": "source",
        "paramReturnId": "getSlotIdForCoursePage",
        "semSubId": sem_id,
        "authorizedID": auth_id, 
        "x": get_curr_time_vtop_format()
}