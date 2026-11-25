import pytest
import allure

from config.settings import USER_DATA
from api.users import Users

@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.api
@allure.title("Test Users Api")
class TestUsersApi:
    def test_user_login(self,seeded_user):
        user_login = seeded_user.login()
        with allure.step("Assert login status and user id"):
            assert user_login.status == 200
            assert seeded_user.get_id()