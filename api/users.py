from playwright.sync_api import APIResponse
import allure

from api.client import ApiClient

class Users:
    def __init__(self,client: ApiClient,user_data:dict,is_admin:bool=False):
        self.client = client
        self.logger = self.client.logger
        self.user_data = user_data
        self.is_admin = is_admin

    def get_id(self):
        return self.user_data.get("id") if self.user_data.get("id") else None

    def get_token(self):
        return self.client.token
    
    @allure.step("User Log in")
    def login(self) -> APIResponse:
        endpoint = "users/login"
        self.logger.info(f"login with {self.user_data["email"]}")
        response = self.client.post(endpoint,
                data={"email":self.user_data["email"], "password":self.user_data["password"]})
        if response.status == 200:
            self.logger.info(f"Login request {self.user_data["email"]} successfully")
            token = response.json().get("access_token")
            if token is not None:
                self.client.set_token(token)
        return response

    @allure.step("Register new user")
    def register(self) -> APIResponse:
        endpoint = "users/register"
        self.logger.info(f"register new user {self.user_data["email"]}")
        response = self.client.post(endpoint,data=self.user_data)
        if response.status == 201:
            self.user_data["id"] = response.json().get("id")
            self.logger.info(f"Register user id {self.user_data["id"]} successfully")
        return response

    @allure.step("Admin delete user id")
    def delete_user(self,user_id) -> APIResponse:
        if self.is_admin:
            response = self.client.delete(f"users/{user_id}",auth=True)
            if response.status == 204:
                self.logger.info(f"User ID {user_id} deleted successfully")
            return response

    @allure.step("Get User detail")
    def get_user_info(self) -> APIResponse: # get user id
        self.logger.info(f"get user detail - users/me")
        response = self.client.get("users/me",auth = True)
        if response.status == 200:
            self.user_data["id"] = response.json().get("id")
            self.logger.info(f"get user {self.user_data["id"]} detail successfully")
        return response

    @allure.step("User Logout")
    def logout(self):
        response = self.client.get("users/logout",auth=True)
        if response.status == 200:
            msg = f"User logout successfully" if not self.is_admin else "Admin logout successfully"
            self.client.set_token(None)
            self.logger.info(msg)
            return response