import pytest
import allure
from config.settings import Settings,LOG_DIR

# --------------------------------------------------------------
# CLI Options 
# --------------------------------------------------------------
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--sprint",type=int, default=5)

@allure.title("Test sprint setup")
@pytest.fixture(scope="session")
def settings(request:pytest.FixtureRequest) -> Settings:
    return Settings(sprint=request.config.getoption("--sprint"))

# --------------------------------------------------------------
# Logger
# --------------------------------------------------------------
from datetime import datetime
def pytest_configure(config) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    config.option.log_file = str(LOG_DIR/f"run_{timestamp}.log")

# --------------------------------------------------------------
# Sprint Specific Testcase
# --------------------------------------------------------------

@pytest.fixture(autouse=True)
def _skip_sprint_without_features(request,settings):
    if request.node.get_closest_marker("auth") and settings.sprint < 4:
        pytest.skip(f"Auth feature not available yet in sprint {settings.sprint}")

# --------------------------------------------------------------
# API context
# --------------------------------------------------------------
from playwright.sync_api import Playwright,APIRequestContext
from api.client import ApiClient

@pytest.fixture(scope="session")
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

# --------------------------------------------------------------
# UI page
# --------------------------------------------------------------

@pytest.fixture
def browser_context_args(browser_context_args:dict,settings:Settings):
    return {**browser_context_args, "base_url" : settings.ui_url}
