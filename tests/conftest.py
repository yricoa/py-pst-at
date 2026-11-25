import pytest
import allure
from config.settings import Settings,LOG_DIR,USER_DATA

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
import logging

@pytest.fixture(scope="session")
def make_session(playwright:Playwright,settings:Settings):
    contexts : list[APIRequestContext] = []

    def _create() -> ApiClient:
        ctx = playwright.request.new_context(base_url=settings.api_url)
        contexts.append(ctx)
        api_client = ApiClient(request_context=ctx,logger=logging.getLogger(__name__))
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

# --------------------------------------------------------------
# Seeding
# --------------------------------------------------------------
from api.users import Users

@pytest.fixture(scope="session")
def admin_user(make_session):
    admin = Users(make_session(),USER_DATA["admin"],is_admin=True)
    admin.login()
    yield admin
    admin.logout()

@pytest.fixture(scope="session")
@allure.title("Seeding test user")
def seeded_user(make_session,worker_id,admin_user):
    user_data = USER_DATA["seeded_user"]
    user_data["email"] = f"new_jack_{worker_id}@gmail.com"
    seeded_user = Users(client=make_session(),user_data=user_data) 
    seed_user_reg_resp = seeded_user.register() # Register response return ID

    # User already exists get ID by get_user_info()
    if "A customer with this email address already exists" in str(seed_user_reg_resp.json().get("email")): 
        login_resp = seeded_user.login()
        if login_resp.status == 200:
            seeded_user.get_user_info()

    yield seeded_user

    # Clean up
    if not seeded_user.get_token():
        seeded_user.logout()
    admin_user.delete_user(seeded_user.user_data["id"])

    