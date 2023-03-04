"""
Gives the faculty detials form the vtop server

Usage:
------
> from vtop_handler import get_faculty_details
> 
> async def main():
>   async with aiohttp.ClientSession() as sess:
>       fac_details = await get_faculty_details()
>       print(fac_details)
>
> asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
> asyncio.run(main())

"""
import asyncio
from typing import Dict, Union, List
import aiohttp

from ..parsers import parse_faculty_details
from .constants import VTOP_FACULTY_URL


async def get_faculty_details()-> Union[List[Dict[str, str]], None]:
    """
    fetches faculty details from the vtop server
    
    Returns:
    ------
        faculty_details: dict
            The faculty details is of the form

            {
              |  'img':"https://someroute.jpg",            // the url of the image
              |  'name':"some facutly name <title>",           // the name of the faculty
              |  'specialization':"some specialization", // the specialization of the faculty
            }

    """
    faculty_details = None
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url=VTOP_FACULTY_URL) as resp:
            faculty_html =  await resp.text()
            faculty_details = parse_faculty_details(faculty_html)


    return faculty_details

async def main():
        res = await get_faculty_details()
        print(res)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # type: ignore
    asyncio.run(main())