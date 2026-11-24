from playwright.sync_api import Page,expect

from config.settings import Settings, Element
from .base_page import BasePage
from .account_page import AccountPage

class LoginPage(BasePage):
    ENDPOINT = "auth/login"
    def __init__(self,page:Page, settings: Settings):
        super().__init__(page=page,settings=settings,endpoint=self.ENDPOINT,load_verify="h3:has-text('Login')")
        self.email_address = Element("input#email","Login Page Email Input")
        self.password = Element("input#password","Login Page Password Input")
        self.login_btn = Element("input[data-test='login-submit']","Login Page Login Submit Button")

    def login(self,user:dict):
        self.fill(self.email_address,user["email"])
        self.fill(self.password,user["password"])
        self.click(self.login_btn)
        return AccountPage(page=self.page,settings=self.settings)