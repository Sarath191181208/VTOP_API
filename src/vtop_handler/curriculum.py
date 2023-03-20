from typing import Callable

import aiohttp

from src.vtop_handler.models.curriculm_models import CurriculumInfo

from .parsers import get_curriculum
from .payloads import get_my_curriculum_payload
from .constants import CURRICULUM_PAGE_URL, HEADERS
from .utils import may_throw


async def send_request(
        sess: aiohttp.ClientSession,
        url: str,
        payload: dict,
        parse_func: Callable
):
    async with sess.post(url, data=payload, headers=HEADERS) as resp:
        html = await resp.text()
        return parse_func(html)
    
@may_throw
async def get_curriculum_info(
    sess: aiohttp.ClientSession, roll_no: str) -> CurriculumInfo:
    payload = get_my_curriculum_payload(roll_no)
    return await send_request(sess, CURRICULUM_PAGE_URL, payload, get_curriculum)