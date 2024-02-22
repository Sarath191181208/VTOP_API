from typing import List, Union
from pydantic import BaseModel


class SingleCurriculumCourse(BaseModel):
    code: str
    course_title: str
    course_type: str
    credits: int

class CreditInfo(BaseModel):
    category: str
    credits: int


class CurriculumInfo(BaseModel):
    credit_info: List[CreditInfo]
    programme_core: List[SingleCurriculumCourse]
    programme_elective: List[SingleCurriculumCourse]
    university_core: List[SingleCurriculumCourse]
    university_elective: List[SingleCurriculumCourse]
