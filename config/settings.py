from dotenv import load_dotenv
import os
import json
from pathlib import Path

load_dotenv()
TEST_DATA_DIR = Path(__file__).parent.parent/"data"

class Settings:
    domain = os.getenv("DOMAIN")
    def _load_json(_path) -> dict:
        try:
            with open(_path,"r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Couldn't find file at\n{_path}")
        
    
    #URLS
    BASE_URL = f"https://{domain}"
    BASE_API_URL = f"https://api.{domain}"

    #DATA DICT
    USER_DATA = _load_json(TEST_DATA_DIR/"users.json")