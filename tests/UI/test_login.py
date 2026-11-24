import pytest
import allure
from playwright.sync_api import Page

from config.settings import USER_DATA, Settings
from pages.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.ui
class TestLogin:
    def test_login_success(self,page:Page,settings:Settings):
        with allure.step("Navigating to login page"):
            login_page = LoginPage(page=page,settings=settings)
            login_page.navigate()
        with allure.step("Verify Login page loaded"):
            assert login_page.wait_for_page_load()
        with allure.step("Login into My Account page"):
            account_page = login_page.login(USER_DATA["test_user2"])
        with allure.step("Verify My Account page loaded"):
            assert account_page.wait_for_page_load()