from typing import List
import pandas as pd

from src.vtop_handler.models.curriculm_models import ( 
    CreditInfo, CurriculumInfo, SingleCurriculumCourse)


def _parse_programme_info_tables(table_df: pd.DataFrame
                                 ) -> List[SingleCurriculumCourse]:
    courses = []
    for row in table_df.itertuples():
        course = SingleCurriculumCourse(
            basket_title=row[2],
            code=row[3],
            course_title=row[4],
            type=row[5],
            credits=row[6],
            is_compulsory=row[7] == "Compulsory",
            registration_status=not pd.isna(row[8]),
            registered_semester=row[9] if not pd.isna(row[9]) else None,
            grade=row[10] if not pd.isna(row[10]) else None
        )
        courses.append(course)
    return courses


def _parse_credit_info(credit_info_df: pd.DataFrame) -> List[CreditInfo]:
    if credit_info_df.empty:
        return []
    # reomve the first row and second as they are headers
    credit_info_df = credit_info_df.iloc[2:]
    return [
        CreditInfo(
            category=row[2],
            credits=row[3]
        ) for row in credit_info_df.itertuples()]


def _parse_tables(df: List[pd.DataFrame]) -> List[List[SingleCurriculumCourse]]:
    return [_parse_programme_info_tables(table_df) for table_df in df]


def get_curriculum(my_cirricum_html: str) -> CurriculumInfo:

    df = pd.read_html(my_cirricum_html)

    credit_info = _parse_credit_info(df[0])
    credits_distribution_info = _parse_tables(df[1:])

    return CurriculumInfo(
        credit_info=credit_info,
        programme_core=credits_distribution_info[0],
        programme_elective=credits_distribution_info[1],
        university_core=credits_distribution_info[2],
        university_elective=credits_distribution_info[3]
    )
