"""
Gives the academic calenders form the vtop server

Usage:
------
> from vtop_handler import get_academic_calender
> 
> async def main():
>   async with aiohttp.ClientSession() as sess:
>       acad_calenders = await get_academic_calender()
>       print(acad_calenders)
>
> asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
> asyncio.run(main())

"""
import asyncio
from typing import Union
import aiohttp

from ..parsers import parse_academic_calender
from .constants import VTOP_ACAD_CALENDER_URL

async def get_academic_calender():
    """
    fetches academic calender from the vtop server
    
    Returns:
    ------
    academic_calenders: list[str]
        The academic calender is of the form
        [
        |    'https://vitap.ac.in/wp-content/uploads/2022/05/Fast-Track-FALL-2022-23.jpg',
        |    'https://vitap.ac.in/wp-content/uploads/2022/01/Winter-semister-2021-22.jpg',
        |    'https://vitap.ac.in/wp-content/uploads/2022/03/EAPCET-Winsem.jpg'
        ]


    """
    academic_calenders = None
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url=VTOP_ACAD_CALENDER_URL) as resp:
            acad_calender_html =  await resp.text()
            academic_calenders = parse_academic_calender(acad_calender_html)

    return academic_calenders

async def main():
        res = await get_academic_calender()
        print(res)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # type: ignore
    asyncio.run(main())