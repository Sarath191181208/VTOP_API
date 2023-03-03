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