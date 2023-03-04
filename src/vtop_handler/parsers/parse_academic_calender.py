from bs4 import BeautifulSoup


from typing import List


def parse_academic_calender(acad_calender_html:str)-> List[str]:
    img_links = []
    try:
        soup = BeautifulSoup(acad_calender_html, "html.parser")
        divs = soup.find_all("center")
        _find_img = lambda div: div.find_all("img")[1].get("src")
        img_links = [_find_img(div) for div in divs]
    except Exception as e:
        print(e)
    return img_links