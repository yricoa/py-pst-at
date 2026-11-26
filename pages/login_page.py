from playwright.sync_api import Page
import allure

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
        self.invalid_user_cred_alert = Element("//div[contains(text(),'Invalid email or password')]","Login Page invalid user credentials alert")
        self.invalid_email_format = Element("//div[contains(text(),'Email format is invalid')]","Login Page invalid email alert")

    def fill_login(self,user:dict):
        self.fill(self.email_address,user["email"])
        self.fill(self.password,user["password"])

    def click_login_btn(self):
        self.click(self.login_btn)

    def invalid_user_cred_popup(self):
        self.wait_for_element_visible(self.invalid_user_cred_alert)

    def invalid_email_popup(self):
        self.wait_for_element_visible(self.invalid_email_format)

    def login(self,user_data:dict):
        self.navigate()
        assert self.wait_for_page_load()
        self.fill_login(user_data)
        self.click_login_btn()