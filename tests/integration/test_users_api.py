import pytest
import allure
from datetime import datetime as dt

from config.settings import USER_DATA
from api.users import Users

@pytest.mark.auth
@pytest.mark.api
@allure.title("Test Users API Integration")
class TestUsersApi:

    @pytest.mark.smoke
    @allure.title("TC001")
    def test_user_login(self,seeded_user):
        user_login = seeded_user.login()
        with allure.step("Assert login status and user id"):
            assert user_login.status == 200
            assert seeded_user.get_id()

    @allure.title("TC002")
    def test_register_new_user(self,seeded_user):
        with allure.step("Assert register status"):
            assert seeded_user.get_user_info().status == 200

    @allure.title("TC003")
    def test_negative_login(self,make_session):
        invalid_user = Users(make_session(),USER_DATA["invalid_user_password"]).login(is_setup_call=True)
        with allure.step("Invalid User cannot login"):
            assert invalid_user.status == 401
            assert "Unauthorized" in str(invalid_user.json().get("error"))

    @allure.title("TC004")
    def test_logout_token_clearing(self,seeded_user):
        with allure.step("Get valid user login token"):
            seeded_user.login()
            token = seeded_user.get_token()
        with allure.step("Logout user"):
            seeded_user.logout()
        with allure.step("Reset cleared client token when logout"):
            seeded_user.client.set_token(token) 
            user_info_resp = seeded_user.get_user_info(is_setup_call=True)
            seeded_user.client.set_token(None)
        with allure.step("Verify login token unusable"):
            assert user_info_resp.status == 401

    @allure.title("TC005")
    def test_user_profile_update(self,seeded_user,new_user_data:dict = USER_DATA["profile_update_fields"]):
        suffix = f"_{str(dt.now().strftime("%M"))}_{str(dt.now().strftime("%f")[-3:])}"
        new_user_data["email"] = f"updated_user_{suffix}@gmail.com"
        with allure.step("Update profile api call"):
            update_profile_resp = seeded_user.update_profile(new_user_data)
            assert update_profile_resp.status == 200
        with allure.step("Verify profile updated"):
            user_profile_after_update = seeded_user.get_user_info().json()
            assert all(user_profile_after_update.get(k) == v for k,v in new_user_data.items())

    @allure.title("TC006")
    def test_user_change_password(self,seeded_user,make_session,new_password:str = "br@ndnEwPassword1"):
        with allure.step("Change password api call"):
            change_password_resp = seeded_user.change_password(new_password)
            assert change_password_resp.status == 200
        with allure.step("Verify login with new password"):
            login_new_password_resp = Users(make_session(), {
                "email" : seeded_user.user_data["email"],
                "password" : new_password}).login()
            assert login_new_password_resp.status == 200