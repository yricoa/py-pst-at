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
        with allure.step(f"Navigating to {self.page.url}/{self.endpoint}"):
            self.page.goto(self.endpoint)

    def wait_for_page_load(self):
        with allure.step(f"Verify {self.endpoint} page loaded"):
            expect(self.load_verify).to_be_visible(timeout=10000)
            self.page.wait_for_timeout(1000)
            return self.load_verify.is_visible()

    def fill(self, ele: Element, text: str):
        with allure.step(f"Filling {ele.desc}"):
            locator = self.page.locator(ele.locator)
            if locator.is_visible():
                self.logger.info(f"Typing into {ele.desc}")
                locator.fill(text)
                self.page.wait_for_timeout(300)
            else:
                self.logger.info(f"{ele.desc} not found")

    def click(self,ele:Element):
        with allure.step(f"Clicking {ele.desc}"):
            locator = self.page.locator(ele.locator)
            if locator.is_visible():
                self.logger.info(f"Clicking {ele.desc}")
                locator.scroll_into_view_if_needed()
                locator.click()
                self.page.wait_for_timeout(500)
            else:
                self.logger.info(f"{ele.desc} not found")

    def select(self,ele:Element,label:str):
        with allure.step(f"Select {label} from {ele.desc}"):
            locator = self.page.locator(ele.locator)
            if locator.is_visible():
                self.logger.info(f"Selecting from {ele.desc}")
                locator.select_option(label=label)
            else:
                self.logger.info(f"{ele.desc} not found")

    def wait_for_element_visible(self,ele:Element):
        with allure.step(f"Wait for {ele.desc} visible"):
            locator = self.page.locator(ele.locator)
            expect(locator).to_be_visible(timeout=10000)
            self.page.wait_for_timeout(500)
            return locator.is_visible(timeout=5000)

    def wait_for_element_disappear(self,ele:Element):
        with allure.step(f"Wait for {ele.desc} to be invisible"):
            locator = self.page.locator(ele.locator)
            expect(locator).to_be_visible(timeout=10000)
            expect(locator).to_be_hidden(timeout=10000)
            self.page.wait_for_timeout(500)

    def wait_for_element_have_text(self,ele:Element,text:str,negative:bool=False):
        with allure.step(f"Wait for {ele.desc} to have text" if not negative else
                         f"Wait for {ele.desc} to not have text"):
            locator = self.page.locator(ele.locator)
            if negative:
                expect(locator).not_to_contain_text(text,timeout=10000)
            else:
                expect(locator).to_contain_text(text,timeout=10000)
            self.page.wait_for_timeout(500)