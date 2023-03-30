from typing import Any, Dict, Hashable, List, Union
import aiohttp

from .parsers import parse_marks_page
from .payloads import get_marks_view_payload
from .constants import HEADERS, MARKS_VIEW_PAGE

marksObjectType = Dict[str, Union[str, None]]
marksItemType = Union[List[marksObjectType], str, None, int, float]


async def get_marks_dict(
    sess: aiohttp.ClientSession,
    roll_no: str,
    sem_id: str
) -> List[Dict[Hashable, marksItemType]]:
    payload = get_marks_view_payload(sem_id, roll_no)
    async with sess.post(MARKS_VIEW_PAGE, data=payload, headers=HEADERS) as resp:
        html = await resp.text()
        return parse_marks_page(html)
