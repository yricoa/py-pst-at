import pytest
import allure
from playwright.sync_api import Page
from datetime import datetime

from config.settings import USER_DATA, Settings
from pages.login_page import LoginPage


@pytest.mark.auth
@pytest.mark.ui
class TestUsers:

    @pytest.mark.smoke
    @allure.title("TC101")
    def test_login_success(self,login_page,account_page,seeded_user):
        with allure.step("Login into My Account page"):
            login_page.login(seeded_user.user_data)
        with allure.step("Verify My Account page loaded"):
            assert account_page.wait_for_page_load()

    @allure.title("TC102")
    def test_register_success(self,register_page,login_page,reg_user_cleanup):
        reg_user_data = USER_DATA["new_user"]
        reg_user_data["email"] = f"reg_user_{datetime.now().strftime("%h%M%S")}@gmail.com"
        with allure.step("Navigating to register page"):
            register_page.navigate()
        with allure.step("Verify register page loaded"):
            register_page.wait_for_page_load()
        with allure.step("Filling register user information"):
            register_page.enter_register_info(reg_user_data)
        with allure.step("Click register submit button"):
            register_page.click_submit_btn()
        reg_user_cleanup(reg_user_data)
        with allure.step("Verify Login Page redirect"):
            login_page.wait_for_page_load()

    @allure.title("TC103")
    @pytest.mark.parametrize("invalid_user_type",("invalid_user_password","invalid_user_email"))
    def test_negative_login(self,login_page,invalid_user_type):
        invalid_user = USER_DATA[invalid_user_type]
        with allure.step("Login with invalid user cred"):
            login_page.login(invalid_user)
        with allure.step("Verify error when submit"):
            if invalid_user_type == "invalid_user_password":
                login_page.invalid_user_cred_popup()
            else:
                login_page.invalid_email_popup()

    @allure.title("TC104")
    def test_user_logout(self,seeded_user,login_page,account_page):
        with allure.step("Login into My Account page"):
            login_page.login(seeded_user.user_data)
        with allure.step("Verify My Account page loaded"):
            assert account_page.wait_for_page_load()
        with allure.step("Logout"):
            account_page.log_out()
        with allure.step("Verify Login page redirect"):
            assert login_page.wait_for_page_load()

    @allure.title("TC105")
    def test_user_update_profile(self,seeded_user,login_page,account_page,profile_page):
        update_profile = USER_DATA["profile_update_fields"]
        with allure.step("Login into My Account page"):
            login_page.login(seeded_user.user_data)
        with allure.step("Verify My Account page loaded"):
            assert account_page.wait_for_page_load()
        with allure.step("Navigating to Profile Page"):
            account_page.click_profile_button()
        with allure.step("Verify Profile Page fully loaded"):
            profile_page.wait_for_page_load()
            # profile_page.wait_for_fully_loaded(loaded_email_text=seeded_user.user_data["email"])
        with allure.step("Update user profile in Profile Page"):
            profile_page.update_user_profile(update_profile)
        with allure.step("Wait for update success alert"):
            profile_page.is_profile_update_success()

    @allure.title("TC106")
    def test_user_change_password(self,seeded_user,login_page,account_page,profile_page,new_password:str = "br@ndnEwPassword1"):
        with allure.step("Login into My Account page"):
            login_page.login(seeded_user.user_data)
        with allure.step("Verify My Account page loaded"):
            assert account_page.wait_for_page_load()
        with allure.step("Navigating to Profile Page"):
            account_page.click_profile_button()
        with allure.step("Verify Profile Page fully loaded"):
            profile_page.wait_for_page_load()
            # profile_page.wait_for_fully_loaded(loaded_email_text=seeded_user.user_data["email"])
        with allure.step("Change password in Profile Page"):
            profile_page.change_password(old_password=seeded_user.user_data["password"],new_password=new_password)
        with allure.step("Wait for update success alert"):
            profile_page.is_change_password_success()
    