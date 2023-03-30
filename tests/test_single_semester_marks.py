import asyncio
import aiohttp
import pytest

from vtop_handler import generate_session
from vtop_handler.marks_view import get_marks_dict


from user_names_passwords import username_password_list, merge_username_passwords


@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, sem_id", merge_username_passwords(
    username_password_list,
    [  "AP2022236",  
       "AP2022236",  
       "AP2022237",  
       "AP2022236"])) 
async def test_single_sem_marks_view(username: str, password: str, sem_id: str):
    async with aiohttp.ClientSession() as sess:
        roll_no = await generate_session(username, password, sess)
        cookie = sess.cookie_jar.filter_cookies(
            'https://vtop2.vitap.ac.in/vtop').get('JSESSIONID').value  # type: ignore
        assert cookie is not None, "Login Failed! No cookie found"
        cookies = {'JSESSIONID': cookie, "loginUserType": "vtopuser"}
        async with aiohttp.ClientSession(cookies=cookies) as sess:
            roll_no = roll_no if roll_no else username
            marks_dict = await get_marks_dict(sess, roll_no, sem_id)

            assert marks_dict is not None, "Failed to get marks dict"
            assert len(marks_dict) > 0, "Failed to get marks dict"

            for k in marks_dict:
                assert k is not None, f"Failed to get marks for {k}"
