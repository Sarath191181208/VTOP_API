import base64
from typing import Dict
from bs4 import BeautifulSoup
import pandas as pd

from ..utils import find_image, nan_to_none_in_dict


def parse_profile(profile_html: str) -> Dict:
    img_col = BeautifulSoup(profile_html, 'lxml').find(id='1a')
    base64_img = find_image(str(img_col))
    raw_df = pd.read_html(profile_html)
    df_personal_info = raw_df[0]
    df_proctor_info = raw_df[3]

    application_number = df_personal_info.iloc[1, 1]

    # getting proctor info
    proctorMobileNumber = None
    try:
        proctorMobileNumber = df_proctor_info.iloc[9, 2]
    except IndexError:
        ...

    # Generating an API Token
    api_gen = application_number
    api_token = api_gen.encode('ascii') # type: ignore
    temptoken = base64.b64encode(api_token)
    token = temptoken.decode('ascii')

    return nan_to_none_in_dict({
        "name": df_personal_info.iloc[2, 1],
        "branch": df_personal_info.iloc[21, 1],
        "program": df_personal_info.iloc[19, 1],
        "regNo": df_personal_info.iloc[18, 1],
        "appNo": df_personal_info.iloc[1, 1],
        "school": df_personal_info.iloc[21, 1],
        "email": df_personal_info.iloc[31, 1],
        "proctorEmail": df_proctor_info.iloc[7, 1],
        "proctorName": df_proctor_info.iloc[2, 1],
        "proctorMobileNumber": proctorMobileNumber,
        "profileImageBase64": base64_img,
        'token': token
    })
