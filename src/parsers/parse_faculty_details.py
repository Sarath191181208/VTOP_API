from bs4 import BeautifulSoup
from typing import Dict, List

import bs4

def _clean_text(text:str)->str:
    chars = ['\n', '\t', '\r']
    text = text.strip()
    for char in chars:
        text = text.replace(char, '')
    return text


def _get_single_fac_detils(div: bs4.element.Tag) -> Dict:
    p_s = div.find_all('p')
    img_link = p_s[0].find_all('img')[1].get('src')
    name = p_s[1].text
    specialization = p_s[2].text

    return {
        'img': _clean_text(img_link),
        'name': _clean_text(name),
        'specialization': _clean_text(specialization)
    }


def parse_faculty_details(fac_html:str)-> List[Dict]:
    fac_details = []
    try:
        soup = BeautifulSoup(fac_html, 'html.parser')
        res = soup.find_all('div', {'class': 'col-md-2 shadow margin-T30'})
        fac_details = [_get_single_fac_detils(div) for div in res]
    except Exception as e:
        print(e)
    return fac_details