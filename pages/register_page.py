from playwright.sync_api import Page

from config.settings import Settings,Element
from pages.base_page import BasePage

class RegisterPage(BasePage):
    ENDPOINT = "auth/register"
    load_verify = "h3:has-text('Customer registration')"

    def __init__(self,page:Page,settings:Settings):
        super().__init__(page,settings,self.load_verify,self.ENDPOINT)
        self.first_name = Element("input#first_name","Register Page first name Input")
        self.last_name = Element("input#last_name","Register Page last name Input")
        self.dob = Element("input#dob","Register Page day of birth Input")
        self.country = Element("select#country","Register Page country drop list")
        self.postal_code = Element("input#postal_code","Register Page postal code Input")
        self.house_number = Element("input#house_number","Register Page house number Input")
        self.street = Element("input#street","Register Page street Input")
        self.city = Element("input#city","Register Page city Input")
        self.state = Element("input#state","Register Page state Input")
        self.phone = Element("input#phone","Register Page phone Input")
        self.email = Element("input#email","Register Page email Input")
        self.password = Element("input#password","Register Page Password Input")
        self.reg_btn = Element("button[data-test='register-submit']","Register Page register submit Button")
        self.address_lookup_loader = Element("div[data-test='postcode-lookup-loading']","Postcode Lookup Loader")

    def enter_register_info(self,user_data):
        self.fill(self.first_name,user_data["first_name"])
        self.fill(self.last_name,user_data["last_name"])
        self.fill(self.dob,user_data["dob"])
        self.select(self.country,user_data["address"]["country"])
        self.fill(self.postal_code,user_data["address"]["postcode"])
        self.fill(self.house_number,user_data["address"]["house_number"])
        self.wait_for_element_disappear(self.address_lookup_loader)
        self.fill(self.state,user_data["address"]["state"])
        self.fill(self.city,user_data["address"]["city"])
        self.fill(self.street,user_data["address"]["street"])
        self.fill(self.phone,user_data["phone"])
        self.fill(self.email,user_data["email"])
        self.fill(self.password,user_data["password"])

    def click_submit_btn(self):
        self.click(self.reg_btn)
