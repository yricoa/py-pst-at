from api.base import BaseApiClient

class UsersClient(BaseApiClient):
    def login(self,user:dict):
        data = {
            "email":user["email"],"password":user["password"]
            }
        response = self.post("users/login",data=data,auth=False)
        if response.ok:
            print(response.json())
            self.set_token(response.json()["access_token"])
        return response

    def get_current_user(self):
        return self.get("users/me",auth=True)