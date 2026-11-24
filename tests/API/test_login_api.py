import pytest
import allure

from config.settings import USER_DATA
from api.users import Users

@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.api
@allure.title("Test Users Api")
class TestUsersApi:
    def test_user_login(self,make_session):
        user_cred = USER_DATA["test_user2"]
        user = Users(client=make_session())
        user_login = user.login(user_cred)
        assert user_login.status == 200