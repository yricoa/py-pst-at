from playwright.sync_api import Page,Locator,expect
from config.settings import Settings

class BasePage:
    def __init__(self,page:Page, load_verify: str = "",endpoint : str = ""):
        self.page = page
        self.endpoint = endpoint
        self.load_verify = self.page.locator(load_verify)

    def navigate(self):
        self.page.goto(self.endpoint)

    def wait_for_page_load(self):
        expect(self.load_verify).to_be_visible()
        return self.load_verify.is_visible()