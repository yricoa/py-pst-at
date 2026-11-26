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

    def set_id(self,id):
        self.user_data["id"] = id

    def get_token(self):
        return self.client.token
    
    def login(self,is_setup_call:bool=False) -> APIResponse:
        with allure.step(f"Login Request: User {self.user_data["email"]}"):
            self.logger.info(f"login with {self.user_data["email"]}")
            response = self.client.post("users/login",
                    data={"email":self.user_data["email"], "password":self.user_data["password"]})
            if not is_setup_call: assert response.status == 200
            self.logger.info(f"Login request {self.user_data["email"]} successfully")
            token = response.json().get("access_token")
            if token is not None:
                self.client.set_token(token)
            return response

    def register(self,is_setup_call:bool=False) -> APIResponse:
        with allure.step(f"Register Request: User {self.user_data["email"]}"):
            response = self.client.post("users/register",data=self.user_data)
            if not is_setup_call: assert response.status == 201
            self.user_data["id"] = response.json().get("id")
            self.logger.info(f"Register user id {self.user_data["id"]} successfully")
            return response

    def get_user_info(self,is_setup_call:bool=False) -> APIResponse: # get user id
            with allure.step(f"User Detail Request: User {self.user_data["email"]}"):
                if not self.get_token():
                    self.login(is_setup_call=is_setup_call)
                response = self.client.get("users/me",auth = True)
                if not is_setup_call: assert response.status == 200
                self.user_data["id"] = response.json().get("id")
                self.logger.info(f"get user {self.user_data["id"]} detail successfully")
                return response
            
    def update_profile(self,user_data) -> APIResponse:
        with allure.step(f"Update Profile Request: User {self.user_data["email"]}"):
            if "id" not in self.user_data:
                self.get_user_info()
            elif not self.get_token():
                self.login()
            response = self.client.put(f"users/{self.user_data["id"]}",auth=True,data=user_data)
            assert response.status == 200
            self.logger.info(f"User {self.user_data["email"]} update profile successfully")
            return response

    def change_password(self,new_password:str) -> APIResponse:
        with allure.step(f"Change Password Request: User {self.user_data["email"]}"):
            if not self.get_token():
                self.login()
            response = self.client.post("users/change-password", auth=True,
                                        data= {"current_password" : self.user_data["password"],
                                               "new_password" : new_password,
                                               "new_password_confirmation" : new_password})
            assert response.status == 200
            self.logger.info(f"User {self.user_data["email"]} change password successfully")
            return response
        
    def delete_user(self,user_id,is_setup_call:bool=False) -> APIResponse:
        with allure.step(f"Admin Delete Request: User ID: {user_id}"):
            if self.is_admin:
                response = self.client.delete(f"users/{user_id}",auth=True)
                if not is_setup_call: assert response.status == 204
                self.logger.info(f"User ID {user_id} deleted successfully")
                return response

    def logout(self,is_setup_call:bool=False) -> APIResponse:
        with allure.step(f"Logout Request: User {self.user_data["email"]}"):
            response = self.client.get("users/logout",auth=True)
            if not is_setup_call: assert response.status == 200
            msg = f"User {self.user_data["email"]} logout successfully" if not self.is_admin else "Admin logout successfully"
            self.client.set_token(None)
            self.logger.info(msg)
            return response