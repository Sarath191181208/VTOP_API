from src.app import app
import os 

PORT = os.getenv("PORT", 5000) 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT))
