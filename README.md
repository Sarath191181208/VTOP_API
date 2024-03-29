Quick Navigation:

- [Description](#description)
- [How to start the server ? (Python \>= 3.9)](#how-to-start-the-server--python--39)
- [How to install this project ?](#how-to-install-this-project-)
- [How does the captcha solving work ?](#how-does-the-captcha-solving-work-)
- [Change the vtop\_handler for any change in the vtop website](#change-the-vtop_handler-for-any-change-in-the-vtop-website)

## Description

An asynchronus way for working with the vtop website.
Inspired from the project VITASK from our peers at VIT-Chennai I tried an asynchronous way of working with the vtop website.
[VITASK](https://github.com/Codebotics/VITask)

Brief Overview:

- We mainly uses aiohttp for requests i.e working with the website.
- Pandas for parsing the data. And BeautifulSoup too.
- The project is mainly wirtten in python 3.9.
- The project is present in the src directory.
- See the vtop_handler_examples.py for examples on how to use the vtop_handler package.

## How to start the server ? (Python >= 3.9)
- Download all the dependencies `pip install -r requirements.in`
- Run the shell command `sh start.sh`

## How to install this project ?

1. Clone the repo

```bash
 git clone https://github.com/Sarath191181208/VTOP_API
```

2. Install the requirements

```bash
 pip install -r requirements.txt
```

3. To run the server
   To run the app go to **src/** folder and then run

```bash
 python app.py
```

## How does the captcha solving work ?

All the characters are saved in vtop_handler/bitmaps.json. The captcha is solved by comparing the bitmaps of the captcha with the bitmaps of the characters. This gives us an accuracy score of letters for every letter in the captcha ,we pick the max letter which has the highest accuracy score.
see in vtop_handler/session_generator.py it has \_solve_captcha function for how it is implemented.

## Change the vtop_handler for any change in the vtop website

- **What if the url's of the vtop website change?**
  Go to vtop_handler/constats.py and change the url's of the vtop website.

- **What if the payloads of the vtop website change?**
  Go to vtop_handler/payloads.py and change the payloads of the vtop website.

- **What if the website of the vtop website change?**
  Go to vtop_handler/ and the part of the website that you want to change. ex: vtop_handler/student_timetable.py and edit the parser of the website.
