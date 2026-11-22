from playwright.sync_api import Page

from config.settings import USER_DATA
from pages.login_page import LoginPage


def test_login_success(page:Page,settings):
    login_page = LoginPage(page=page,settings=settings)
    login_page.navigate()
    assert login_page.wait_for_page_load()
    account_page = login_page.login(USER_DATA["test_user"])
    assert account_page.wait_for_page_load()