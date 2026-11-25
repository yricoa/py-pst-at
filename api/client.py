import logging
from playwright.sync_api import APIRequestContext,APIResponse

class ApiClient:
    success_code = [200,201,204]
    def __init__(self,request_context:APIRequestContext,logger:logging.Logger):
        self.request = request_context
        self.token : str | None = None
        self.logger = logger

    def build_headers(self, auth:bool = False, extra_headers:dict[str,str] | None=None):
        headers = {"Accept" : "application/json"}
        if auth == True and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def set_token(self,token:str):
        self.token = token

    def get(self, endpoint:str | None=None,
            auth:bool = False, extra_headers:dict | None=None) -> APIResponse:
        resp = self.request.get(url=endpoint,headers=self.build_headers(auth,extra_headers))
        if resp.status in self.success_code:
            self.logger.debug(f"GET {endpoint} response status: {resp.status}")
        else:
            self.logger.debug(f"GET {endpoint} failed: {resp.json()}")
        return resp

    def post(self, endpoint:str|None=None, data:dict|None=None,
             auth:bool = False, extra_headers:dict | None=None) -> APIResponse:
        resp = self.request.post(endpoint, headers=self.build_headers(auth,extra_headers), data=data)
        if resp.status in self.success_code:
            self.logger.debug(f"POST {endpoint} response status: {resp.status}")
        else:
            self.logger.debug(f"POST {endpoint} failed: {resp.json()}")
        return resp

    def put(self, endpoint:str | None=None, data:dict| None = None,
            auth:bool = False, extra_headers:dict | None = None) -> APIResponse:
        resp = self.request.put(endpoint, headers=self.build_headers(auth,extra_headers), data=data)
        if resp.status in self.success_code:
            self.logger.debug(f"PUT {endpoint} response status: {resp.status}")
        else:
            self.logger.debug(f"PUT {endpoint} failed: {resp.json()}")
        return resp

    def delete(self, endpoint:str | None=None, data:dict| None = None,
               auth:bool = False, extra_headers:dict | None = None) -> APIResponse:
        resp = self.request.delete(endpoint, headers=self.build_headers(auth,extra_headers), data=data)
        if resp.status in self.success_code:
            self.logger.debug(f"DELETE {endpoint} response status: {resp.status}")
        else:
            self.logger.debug(f"DELETE {endpoint} failed: {resp.json()}")
        return resp