from typing import List, Union
from pydantic import BaseModel


class SingleCurriculumCourse(BaseModel):
    basket_title: str
    code: str
    course_title: str
    type: str
    credits: int
    is_compulsory: bool
    registration_status: bool
    registered_semester: Union[str, None]
    grade: Union[str, None]


class CreditInfo(BaseModel):
    category: str
    credits: int


class CurriculumInfo(BaseModel):
    credit_info: List[CreditInfo]
    programme_core: List[SingleCurriculumCourse]
    programme_elective: List[SingleCurriculumCourse]
    university_core: List[SingleCurriculumCourse]
    university_elective: List[SingleCurriculumCourse]
