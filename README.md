## How does the captcha solving work ?
All the characters are saved in vtop_handler/bitmaps.json. The captcha is solved by comparing the bitmaps of the captcha with the bitmaps of the characters. This gives us an accuracy score of letters for every letter in the captcha ,we pick the max letter which has the highest accuracy score. 
see in vtop_handler/session_generator.py it has _solve_captcha function for how it is implemented.

## Change the vtop_handler for any change in the vtop website 
- **What if the url's of the vtop website change?**
Go to vtop_handler/constats.py and change the url's of the vtop website.

- **What if the payloads of the vtop website change?**
Go to vtop_handler/payloads.py and change the payloads of the vtop website.

- **What if the website of the vtop website change?**
Go to vtop_handler/ and the part of the website that you want to change. ex: vtop_handler/student_timetable.py and edit the parser of the website.