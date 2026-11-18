from playwright.sync_api import APIRequestContext,APIResponse

class BaseApiClient:
    def __init__(self,request_context: APIRequestContext):
        self.request = request_context
        self.token: str | None = None

    def set_token(self,token:str):
        self.token = token

    def clear_token(self):
        self.token = None

    def _build_headers(self,auth: bool = False, extra_headers: dict | None = None) -> dict:
        headers = {"Accept": "application/json"}
        if auth and self.token:
            headers["Authorization"] = self.token
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def get(self,endpoint:str,auth:bool=False) -> APIResponse:
        return self.request.get(endpoint,headers=self._build_headers(auth=auth))

    def post(self,endpoint:str,data:dict|None=None,auth:bool=False) -> APIResponse:
        return self.request.post(endpoint,headers=self._build_headers(auth=auth),data=data)

    def put(self,endpoint:str,data:dict|None=None,auth:bool=False) -> APIResponse:
        return self.request.put(endpoint,headers=self._build_headers(auth=auth),data=data)

    def delete(self,endpoint:str,auth:bool=False) -> APIResponse:
        return self.request.delete(endpoint,headers=self._build_headers(auth=auth))