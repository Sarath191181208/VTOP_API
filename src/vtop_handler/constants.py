VTOP_BASE_URL = r"https://vtop.vitap.ac.in/vtop/"
VTOP_LOGIN_URL = r"https://vtop.vitap.ac.in/vtop/vtopLogin"

VTOP_BASE_URL = r"https://vtop.vitap.ac.in/vtop/open/page"
VTOP_PRE_LOGIN = r"https://vtop.vitap.ac.in/vtop/prelogin/setup"
VTOP_LOGIN_PAGE_REDIRECT = r"https://vtop.vitap.ac.in/vtop/init/page"
VTOP_LOGIN_URL = r"https://vtop.vitap.ac.in/vtop/login"
VTOP_DO_LOGIN_URL = r"https://vtop.vitap.ac.in/vtop/doLogin"

VTOP_ATTENDANCE_URL = r"https://vtop.vitap.ac.in/vtop/processViewStudentAttendance"
VTOP_SINGLE_SUBJECT_ATTENDANCE_URL = (
    r"https://vtop.vitap.ac.in/vtop/processViewAttendanceDetail"
)
VTOP_TIMETABLE_URL = r"https://vtop.vitap.ac.in/vtop/processViewTimeTable"
VTOP_ACADHISTORY_URL = (
    r"https://vtop.vitap.ac.in/vtop/examinations/examGradeView/StudentGradeHistory"
)
VTOP_PROFILE_URL = (
    r"https://vtop.vitap.ac.in/vtop/studentsRecord/StudentProfileAllView"
)
VTOP_MARKS_URL = r"https://vtop.vitap.ac.in/vtop/examinations/doStudentMarkView"
VTOP_EXAM_SCHEDULE_URL = (
    r"https://vtop.vitap.ac.in/vtop/examinations/doSearchExamScheduleForStudent"
)
VTOP_FACULTY_URL = r"https://vitap.ac.in/faculty/"
VTOP_ACAD_CALENDER_URL = r"https://vitap.ac.in/academic-calendar/"

# --- Course page ---
COURSE_PAGE_URL = r"https://vtop.vitap.ac.in/vtop/academics/common/StudentCoursePage"  # for gettting into the page returns-> sem id
COURSE_PAGE_SEMESTER_URL = r"https://vtop.vitap.ac.in/vtop/getCourseForCoursePage"  # for selecting a semester ex: WIN SEM  returns-> subject ids
COURSE_PAGE_SELECT_COURSE_URL = r"https://vtop.vitap.ac.in/vtop/getSlotIdForCoursePage"  # for selecting a course ex: CSE1001 python returns-> table of contents
COURSE_PAGE_GET_CONTENT_URL = (
    r"https://vtop.vitap.ac.in/vtop/processViewStudentCourseDetail"
)

# Marks View
MARKS_VIEW_PAGE = r"https://vtop.vitap.ac.in/vtop/examinations/doStudentMarkView"

# Curriculum URL
CURRICULUM_PAGE_URL = "https://vtop.vitap.ac.in/vtop/academics/common/Curriculum"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}

SEM_IDS = [
    # "AP2022234",
    "AP2023246", # WIN SEM (2023-24)
    # "AP2023241", # FAST TRACK FALL SEM (2023 - 24)
    # "AP2022237",  # WIN SEM FRESHERS (2022 - 23)
    # "AP2022232",
]
