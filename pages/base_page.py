from playwright.sync_api import Page,Locator,expect
from config.settings import Settings as S

class BasePage:
    def __init__(self,page:Page,endpoint: str = "", load_verify: str = ""):
        self.page = page
        self.url = f"{S.BASE_URL}/{endpoint}"
        self.load_verify = self.page.locator(load_verify)

    def navigate(self):
        self.page.goto(self.url)

    def wait_for_page_load(self):
        expect(self.load_verify).to_be_visible()
        return self.load_verify.is_visible()
