from playwright.sync_api import Page,expect

from .base_page import BasePage
from .account_page import AccountPage

class LoginPage(BasePage):
    ENDPOINT = "auth/login"
    def __init__(self,page:Page,settings):
        super().__init__(page=page,settings=settings,endpoint=self.ENDPOINT,load_verify="h3:has-text('Login')")
        self.settings = settings
        self.email_address = self.page.locator("input#email")
        self.password = self.page.locator("input#password")
        self.login_btn = self.page.locator("input[data-test='login-submit']")

    def login(self,user:dict):
        print(user["email"])
        self.email_address.fill(user["email"])
        self.password.fill(user["password"])
        self.login_btn.click()
        return AccountPage(page=self.page,settings=self.settings)
