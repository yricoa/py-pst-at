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
# Seeding
# --------------------------------------------------------------
from api.users import Users
from datetime import datetime as dt

@pytest.fixture(scope="session")
def admin_user(make_session):
    admin = Users(make_session(),USER_DATA["admin"],is_admin=True)
    admin.login()
    yield admin
    admin.logout()

@pytest.fixture
@allure.title("Seeding test user")
def seeded_user(make_session,worker_id,admin_user):
    suffix = f"{worker_id}_{str(dt.now().strftime("%M"))}_{str(dt.now().strftime("%f")[-3:])}"
    user_data = USER_DATA["seeded_user"]
    user_data["email"] = f"new_{suffix}@gmail.com"
    seeded_user = Users(client=make_session(),user_data=user_data) 
    seed_user_reg_resp = seeded_user.register(is_setup_call=True) # Register response return ID
    id = seeded_user.user_data["id"]
    # User already exists get ID by get_user_info()
    if "A customer with this email address already exists" in str(seed_user_reg_resp.json().get("email")): 
        seeded_user.get_user_info(is_setup_call=True)

    yield seeded_user

    # Clean up
    if seeded_user.get_token():
        seeded_user.logout(is_setup_call=True)
    admin_user.delete_user(id)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Capture only when the main test call fails
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page and not page.is_closed():
            allure.attach(
                page.screenshot(full_page=True),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                page.content(),
                name="headless_dom",
                attachment_type=allure.attachment_type.HTML,
            )