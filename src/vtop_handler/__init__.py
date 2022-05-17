"""
Packages of vtop_handler.
---------------------------
Go to the individual package's documentation for more details.

- session_generator.get_valid_session: 
    Login to vtop and get a valid session.

- student_profile.get_student_profile: 
    Get the profile details dictionary of the student.

- student_timetable.get_timetable:
    Get the timetable dictionary of the student.

"""

from vtop_handler import session_generator
from vtop_handler import student_profile
from vtop_handler import student_timetable
from vtop_handler import student_academic_history

from vtop_handler.session_generator import get_valid_session
from vtop_handler.student_profile import get_student_profile
from vtop_handler.student_timetable import get_timetable
from vtop_handler.student_attendance import get_attendance
from vtop_handler.student_academic_history import get_acadhistory