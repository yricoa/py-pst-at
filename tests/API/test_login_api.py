import pytest

from config.settings import USER_DATA
from api.users import Users

def test_user_login(make_session):
    user_cred = USER_DATA["test_user"]
    user = Users(client=make_session())
    user_login = user.login(user_cred)
    assert user_login.status == 200