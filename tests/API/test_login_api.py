from config.settings import Settings

def test_user_login(api):
    user = Settings.USER_DATA["test_user"]
    response = api.users.login(user=user)
    assert response.status == 200