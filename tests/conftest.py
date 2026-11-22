import pytest


from config.settings import Settings


# CLI Options 
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--sprint",type=int, default=5)

@pytest.fixture
def settings(request:pytest.FixtureRequest) -> Settings:
    return Settings(sprint=request.config.getoption("--sprint"))

# API context
from playwright.sync_api import Playwright,APIRequestContext
from api.client import ApiClient

@pytest.fixture
def make_session(playwright:Playwright,settings:Settings):
    contexts : list[APIRequestContext] = []

    def _create() -> ApiClient:
        ctx = playwright.request.new_context(base_url=settings.api_url)
        contexts.append(ctx)
        api_client = ApiClient(request_context=ctx)
        return api_client

    yield _create

    for ctx in contexts: #Tear down
        ctx.dispose()

# UI page
from pages.base_page import BasePage
from playwright.sync_api import Page


@pytest.fixture
def make_page(page: Page, settings:Settings):
    def _create(page_cls,*args,**kwargs):
        return page_cls(page, settings, *args, **kwargs)
    return _create