import re
from typing import Dict, Union
import pandas as pd
import datetime


def find_image(html_str: str) -> Union[str, None]:
    """
    finds the captcha base64 image in the given html

    Explanation:
    ------------

    pattern is like this:
        > src="data:.*;base64,(.*?)"
        ----------------------------
        - src="data: # matches this particular string 
        - .* # matches any character any number of times
        - ;base64, # matches this particular string
        - (.*?) # matches any character any number of times and stores it in a group

    then we are using the group 1 to get the base64 image
    """
    img_pattern = re.compile(r'src="data:.*;base64,(.*?)"')
    img = re.search(img_pattern, html_str)
    if img:
        return img.group(1)
    return None


def null_if_dash(x): return None if x == "-" else x


def get_curr_time_vtop_format() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%c GMT")


def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except:
        return False


def nan_to_none_in_dict(x: Dict) -> Dict:
    """
    converts all the nan values to None in the given dict
    """
    return {k: None if pd.isna(v) else v for k, v in x.items()}
