from playwright.sync_api import Page,expect

from config.settings import Settings
from .base_page import BasePage

class AccountPage(BasePage):
    ENDPOINT = "account"
    def __init__(self,page:Page, settings: Settings):
        super().__init__(page=page,settings=settings,endpoint=self.ENDPOINT,load_verify="h1:has-text('My account')")
