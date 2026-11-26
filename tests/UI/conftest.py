#---------------------------------------------------------------------------
# UI page

import pytest
import allure


#---------------------------------------------------------------------------
# POM fixtures
#---------------------------------------------------------------------------
from playwright.sync_api import Playwright

from config.settings import Settings 
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.account_page import AccountPage,AccountProfilePage

@pytest.fixture(scope="function")
def page(playwright:Playwright, settings:Settings):
    browser = playwright.chromium.launch(args=["--start-maximized"],headless=False)
    ctx = browser.new_context(base_url = settings.ui_url, no_viewport = True)
    yield ctx.new_page()
    ctx.close()
    browser.close()

@pytest.fixture
def login_page(page,settings) -> LoginPage:
    return LoginPage(page,settings)

@pytest.fixture
def register_page(page,settings) -> RegisterPage:
    return RegisterPage(page,settings)

@pytest.fixture
def account_page(page,settings) -> AccountPage:
    return AccountPage(page,settings)

@pytest.fixture
def profile_page(page,settings) -> AccountProfilePage:
    return AccountProfilePage(page,settings)

#---------------------------------------------------------------------------
# Test account clean up
#---------------------------------------------------------------------------
from api.users import Users
@pytest.fixture
@allure.title("Clean up registered test user")
def reg_user_cleanup(make_session,admin_user):
    users_to_delete = []
    def add_this_user(user_data):
        users_to_delete.append(user_data)
    yield add_this_user
    for user_data in users_to_delete:
        user = Users(make_session(),user_data)
        user.login()
        user.get_user_info()
        admin_user.delete_user(user.user_data["id"])