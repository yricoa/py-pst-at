import pytest
from playwright.sync_api import Playwright

from api.client import ApiClient
from config.settings import Settings

@pytest.fixture
def api(playwright: Playwright):
    context = playwright.request.new_context(base_url=Settings.BASE_API_URL)
    client = ApiClient(context)
    yield client
    context.dispose()
