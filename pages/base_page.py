from playwright.sync_api import Page,Locator,expect
import logging
import allure

from config.settings import Settings, Element

class BasePage:
    endpoint = ''
    def __init__(self,page:Page, settings: Settings, load_verify: str = "",endpoint : str = ""):
        self.page = page
        self.settings = settings
        self.endpoint = endpoint if settings.sprint > 4 else f"#/{endpoint}"
        self.load_verify = self.page.locator(load_verify)
        self.logger = logging.getLogger(__name__)

    def navigate(self):
        self.logger.info(f"Go to {self.endpoint}")
        self.page.goto(self.endpoint)

    def wait_for_page_load(self):
        expect(self.load_verify).to_be_visible()
        return self.load_verify.is_visible()

    def fill(self, ele: Element, text: str):
        with allure.step(f"Filling {ele.desc}"):
            locator = self.page.locator(ele.locator)
            if locator.is_visible():
                self.logger.info(f"Typing into {ele.desc}")
                locator.fill(text)
            else:
                self.logger.info(f"{ele.desc} not found")

    def click(self,ele:Element):
        with allure.step(f"Clicking {ele.desc}"):
            locator = self.page.locator(ele.locator)
            if locator.is_visible():
                self.logger.info(f"Clicking {ele.desc}")
                locator.click()
            else:
                self.logger.info(f"{ele.desc} not found")    