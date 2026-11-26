from playwright.sync_api import Page,expect

from config.settings import Settings, Element
from .base_page import BasePage

class AccountPage(BasePage):
    ENDPOINT = "account"
    def __init__(self,page:Page, settings: Settings):
        super().__init__(page=page,settings=settings,endpoint=self.ENDPOINT,load_verify="h1:has-text('My account')")
        self.menu_btn = Element("button#menu","Account Page menu button")
        self.drop_down_menu = Element("//ul[@class='dropdown-menu show']","Account Page drop down menu")
        self.sign_out_btn = Element("a[data-test='nav-sign-out']","Account Page sign out button")
        self.profile_btn = Element("a[data-test='nav-profile']","Account Page profile menu button")

    def log_out(self):
        self.click(self.menu_btn)
        self.wait_for_element_visible(self.drop_down_menu)
        self.wait_for_element_visible(self.sign_out_btn)
        self.click(self.sign_out_btn)

    def click_profile_button(self):
        self.click(self.profile_btn)

class AccountProfilePage(BasePage):
    ENDPOINT = "account/profile"
    def __init__(self,page:Page,settings:Settings):
        page.wait_for_load_state()
        super().__init__(page=page,settings=settings,endpoint=self.ENDPOINT,load_verify="//h1[@data-test='page-title']")
        self.first_name = Element("input#first_name", "Profile Page first name input")
        self.last_name = Element("input#last_name", "Profile Page last name input")
        self.last_name = Element("input#last_name", "Profile Page last name input")
        self.email = Element("input#email", "Profile Page email input")
        self.phone = Element("input#phone", "Profile Page phone input")
        self.street = Element("input#street", "Profile Page street input")
        self.postal_code = Element("input#postal_code", "Profile Page postal code input")
        self.city = Element("input#city", "Profile Page city input")
        self.state = Element("input#state", "Profile Page state input")
        self.country = Element("input#country", "Profile Page country input")
        self.update_profile_btn = Element("button[data-test='update-profile-submit']","Profile Page update profile button")
        self.update_success_alert = Element("button[data-test='update-profile-submit']~div.alert-success","Profile Page update profile success alert")
        self.old_password = Element("input#current-password","Profile Page current password input")
        self.new_password = Element("input#new-password","Profile Page new password input")
        self.new_confirm = Element("input#new-password-confirm","Profile Page new password confirm input")
        self.change_password_btn = Element("button[data-test='change-password-submit']","Profile Page change password button")
        self.change_password_success_alert = Element("button[data-test='change-password-submit']~div.alert-success","Profile Page change password success alert")

    def wait_for_fully_loaded(self,loaded_email_text):
        self.wait_for_element_have_text(self.email,text=loaded_email_text)

    def fill_in_update_profile(self,user_data:dict):
        self.fill(self.first_name,user_data["first_name"])
        self.fill(self.last_name,user_data["last_name"])
        self.fill(self.country,user_data["address"]["country"])
        self.fill(self.postal_code,user_data["address"]["postal_code"])
        self.fill(self.state,user_data["address"]["state"])
        self.fill(self.city,user_data["address"]["city"])
        self.fill(self.street,f"{user_data["address"]["house_number"]} {user_data["address"]["street"]}")
        self.fill(self.phone,user_data["phone"])

    def update_user_profile(self,user_data:dict):
        self.fill_in_update_profile(user_data)
        self.click(self.update_profile_btn)

    def is_profile_update_success(self):
        assert self.wait_for_element_visible(self.update_success_alert)

    def fill_change_password(self,old_password,new_password):
        self.fill(self.old_password,old_password)
        self.fill(self.new_password,new_password)
        self.fill(self.new_confirm,new_password)

    def change_password(self,old_password,new_password):
        self.fill_change_password(old_password,new_password)
        self.click(self.change_password_btn)

    def is_change_password_success(self):
        assert self.wait_for_element_visible(self.change_password_success_alert)