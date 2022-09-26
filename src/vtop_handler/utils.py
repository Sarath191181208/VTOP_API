import re
from typing import Union


def find_image(html_str:str) -> Union[str, None]:
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
