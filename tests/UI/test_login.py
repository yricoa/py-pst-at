from playwright.sync_api import Page

from config.settings import Settings
from pages.login_page import LoginPage

class TestLogin:
    def test_login_success(self,page:Page):
        login_page = LoginPage(page=page)
        login_page.navigate()
        assert login_page.wait_for_page_load()
        account_page = login_page.login(Settings.USER_DATA["test_user"])
        assert account_page.wait_for_page_load()
