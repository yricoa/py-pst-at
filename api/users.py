from playwright.sync_api import APIResponse
from api.client import ApiClient

class Users:
    def __init__(self,client: ApiClient):
        self.client = client

    def login(self,user_cred:dict) -> APIResponse:
        response = self.client.post("users/login",data=user_cred)
        if response.status == 200:
            token = response.json().get("access_token")
            if token is not None:
                self.client.set_token(token)
        return response

    def user_info(self) -> APIResponse:
        self.client.get("users/me",auth = True)