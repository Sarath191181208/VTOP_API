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

from . import session_generator
from . import student_profile
from . import student_timetable
from . import student_academic_history
from . import faculty_handler
from . import academic_calender_handler
from . import student_exam_schedule

from .session_generator import get_valid_session, generate_session
from .student_profile import get_student_profile
from .student_timetable import get_timetable
from .student_attendance import get_attendance
from .student_academic_history import get_acadhistory
from .faculty_handler import get_faculty_details
from .academic_calender_handler import get_academic_calender
from .student_exam_schedule import get_exam_schedule