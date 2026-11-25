import pytest
import allure

from config.settings import USER_DATA
from api.users import Users

@pytest.mark.auth
@pytest.mark.api
@allure.title("Test Users Api")
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
            seeded_user.login()
            assert seeded_user.get_user_info().status == 200

    @allure.title("TC003")
    def test_negative_login(self,make_session):
        invalid_user = Users(make_session(),USER_DATA["invalid_user_password"]).login()
        with allure.step("Invalid User cannot login"):
            assert invalid_user.status == 401
            assert "Unauthorized" in str(invalid_user.json().get("error"))

    @allure.title("TC004")
    def test_logout_token_clearing(self,seeded_user):
        test_user,token = seeded_user,""
        with allure.step("Get valid user login token"):
            login_resp = test_user.login()
            token = test_user.get_token()
        with allure.step("Logout user"):
            test_user.logout()
        with allure.step("Reset cleared client token when logout"):
            test_user.client.set_token(token) 
            user_info_resp = test_user.get_user_info()
            test_user.client.set_token(None) 
        with allure.step("Verify login token unusable"):
            assert user_info_resp.status == 401