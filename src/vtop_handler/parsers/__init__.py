"""
    All the parsers for the vtop_handler which take a html string 
    and return a parsed object i.e extracting data from the html files
"""

from .parse_academic_calender import parse_academic_calender
from .parse_acadhistory import parse_acadhistory
from .parse_attendance import parse_attendance
from .profile_parser import parse_profile
from .time_table_parser import parse_timetable

from .parse_exam_schedule import parse_exam_schedule
from .parse_faculty_details import parse_faculty_details

from .parse_course_page import parse_course_page_semester_names, parse_course_names_values, parse_to_get_view_urls, parse_reference_material_links

from .curriculm import get_curriculum
