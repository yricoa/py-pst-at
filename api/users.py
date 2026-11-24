from playwright.sync_api import APIResponse
import allure

from api.client import ApiClient

class Users:
    def __init__(self,client: ApiClient):
        self.client = client
        self.logger = client.logger

    @allure.step("users/login api request")
    def login(self,user_cred:dict) -> APIResponse:
        endpoint = "users/login"
        self.logger.debug(f"login with {user_cred["email"]} - {endpoint}")
        response = self.client.post(endpoint,data=user_cred)
        if response.status == 200:
            self.logger.info(f"Login request {user_cred["email"]} success")
            token = response.json().get("access_token")
            if token is not None:
                self.client.set_token(token)
        return response

    def user_info(self) -> APIResponse:
        self.logger.debug(f"get user detail - users/me")
        self.client.get("users/me",auth = True)
        