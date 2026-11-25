from playwright.sync_api import Page,expect

from config.settings import Settings, Element
from .base_page import BasePage

class AccountPage(BasePage):
    ENDPOINT = "account"
    def __init__(self,page:Page, settings: Settings):
        super().__init__(page=page,settings=settings,endpoint=self.ENDPOINT,load_verify="h1:has-text('My account')")
        self.menu_btn = Element("button#menu","Account Page menu button")
        self.drop_down_menu = Element("//ul[@class='dropdown-menu show']","Account Page drop down menu")
        self.sign_out_btn = Element("a[data-test='nav-sign-out']","Account Page sign out button")

    def log_out(self):
        self.click(self.menu_btn)
        self.wait_for_element_visible(self.drop_down_menu)
        self.wait_for_element_visible(self.sign_out_btn)
        self.click(self.sign_out_btn)