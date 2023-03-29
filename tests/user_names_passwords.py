import os
import dotenv
dotenv.load_dotenv()

USERNAME = os.getenv('VTOP_USERNAME_1', None)
PASSWORD = os.getenv('VTOP_PASSWORD_1', None)
VITEEE_USERNAME_1 = os.getenv('VITEEE_USERNAME_1', None)
VITEEE_PASSWORD_1 = os.getenv('VITEEE_PASSWORD_1', None)
FRESHER_USERNAME_1 = os.getenv('FRESHER_USERNAME_1', None)
FRESHER_PASSWORD_1 = os.getenv('FRESHER_PASSWORD_1', None)

for i in [USERNAME, PASSWORD,
          VITEEE_USERNAME_1, VITEEE_PASSWORD_1,
          FRESHER_USERNAME_1, FRESHER_PASSWORD_1]:
    assert i is not None, "Please set the environment variables"
