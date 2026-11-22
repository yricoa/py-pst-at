from playwright.sync_api import APIRequestContext,APIResponse

class ApiClient:
    def __init__(self,request_context:APIRequestContext):
        self.request = request_context
        self.token : str | None = None

    def build_headers(self, auth:bool = False, extra_headers:dict[str,str] | None=None):
        headers = {"Accept" : "application/json"}
        if auth == True and self.token:
            headers["Authorization"] = self.token
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def set_token(self,token:str):
        self.token = token

    def get(self, endpoint:str | None=None,
            auth:bool = False, extra_headers:dict | None=None) -> APIResponse:
        return self.request.get(url=endpoint,headers=self.build_headers(auth,extra_headers))

    def post(self, endpoint:str|None=None, data:dict|None=None,
             auth:bool = False, extra_headers:dict | None=None) -> APIResponse:
        return self.request.post(endpoint, headers=self.build_headers(auth,extra_headers), data=data)

    def put(self, endpoint:str | None=None, data:dict| None = None,
            auth:bool = False, extra_headers:dict | None = None) -> APIResponse:
        return self.request.put(endpoint, headers=self.build_headers(auth,extra_headers), data=data)

    def delete(self, endpoint:str | None=None, data:dict| None = None,
               auth:bool = False, extra_headers:dict | None = None) -> APIResponse:
        return self.request.delete(endpoint, headers=self.build_headers(auth,extra_headers), data=data)