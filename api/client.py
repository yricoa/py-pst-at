from playwright.sync_api import APIRequestContext

from .endpoints.users_client import UsersClient

class ApiClient:
    def __init__(self,request_context:APIRequestContext):
        self.users = UsersClient(request_context)
        # self.products = ProductsClient(request_context)
        # self.carts = CartsClient(request_context)

    def login_as(self,user:dict):
        response = self.users.login(user)
        assert response.ok
        token = self.users.token
        return token