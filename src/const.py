import dotenv
import os

dotenv.load_dotenv()

IS_DEBUG = bool(os.getenv("DEBUG", False))
PROD_SERVER_URL = ""

CORS_RESOURCE_LIST = {
    r"/api/*": {
        "origins": [
            # if IS_DEBUG else None,
            "http://localhost:5173",
            PROD_SERVER_URL,
            "https://vtop2.vitap.ac.in",
        ]
    },
    r"/": {"origins": "*"},
}
