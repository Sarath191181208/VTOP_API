from typing import Dict
import aiohttp

from .parsers import parse_marks_page
from .payloads import get_marks_view_payload
from .constants import HEADERS, MARKS_VIEW_PAGE

async def   get_marks_dict(
            sess: aiohttp.ClientSession, 
            auth_id: str, 
            sem_id: str
    ) -> Dict[str, str]:
    payload = get_marks_view_payload(sem_id , auth_id)
    async with sess.post(MARKS_VIEW_PAGE, data=payload, headers=HEADERS) as resp:
        html = await resp.text()
        return parse_marks_page(html)
