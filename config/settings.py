from dotenv import load_dotenv
import os
import json
from pathlib import Path
from dataclasses import dataclass, field
from playwright.sync_api import Locator
import logging

load_dotenv()
TEST_DATA_DIR = Path(__file__).parent.parent/"data"
LOG_DIR = Path(__file__).parent.parent/"logs"
DOMAIN = os.getenv("DOMAIN")

def _load_json(_path) -> dict:
    try:
        with open(_path,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Couldn't find file at\n{_path}")

#DATA DICT
USER_DATA = _load_json(TEST_DATA_DIR/"users.json")

@dataclass
class Settings:
    sprint : int
    api_url : str = field(init=False)
    ui_url : str = field(init=False)

    def __post_init__(self)->None:
        sprint = min(self.sprint,5) if self.sprint is not None else 5
        api_prefix = os.getenv(f"APIV{sprint}")
        ui_prefix = os.getenv(f"V{self.sprint}")
        ui_url = f"https://{ui_prefix}.{DOMAIN}" if sprint < 5 else f"https://{DOMAIN}"
        object.__setattr__(self,"api_url",f"https://{api_prefix}.{DOMAIN}")
        object.__setattr__(self,"ui_url",ui_url)

@dataclass
class Element:
    locator : str
    desc : str
