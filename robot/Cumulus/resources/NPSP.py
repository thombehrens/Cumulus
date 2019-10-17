import logging
import warnings
import time

from robot.libraries.BuiltIn import RobotNotRunningError
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from SeleniumLibrary.errors import ElementNotFound
from simple_salesforce import SalesforceMalformedRequest
from simple_salesforce import SalesforceResourceNotFound
from selenium.webdriver import ActionChains
from cumulusci.robotframework.utils import selenium_retry
from email.mime import text

from cumulusci.tasks.apex.anon import AnonymousApexTask
from cumulusci.core.config import TaskConfig

from tasks.salesforce_robot_library_base import SalesforceRobotLibraryBase


from locators_46 import npsp_lex_locators as locators_46
from locators_47 import npsp_lex_locators as locators_47
locators_by_api_version = {
    47.0: locators_47,   # winter '20
    46.0: locators_46,  # Summer '19
}
# will get populated in _init_locators
npsp_lex_locators = {}

@selenium_retry
class NPSP(SalesforceRobotLibraryBase):
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 1.0

    def __init__(self, debug=False):
        self.debug = debug
        self.current_page = None
        self._session_records = []
        self.val=0
        self.payment_list= []
        # Turn off info logging of all http requests 
        logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARN)
        self._init_locators()

    def _init_locators(self):
        try:
            client = self.cumulusci.tooling
            response = client._call_salesforce(
                'GET', 'https://{}/services/data'.format(client.sf_instance))
            self.latest_api_version = float(response.json()[-1]['version'])
            if not self.latest_api_version in locators_by_api_version:
                warnings.warn("Could not find locator library for API %d" % self.latest_api_version)
                self.latest_api_version = max(locators_by_api_version.keys())
        except RobotNotRunningError:
            # We aren't part of a running test, likely because we are
            # generating keyword documentation. If that's the case, assume
            # the latest supported version
            self.latest_api_version = max(locators_by_api_version.keys())
        locators = locators_by_api_version[self.latest_api_version]
        npsp_lex_locators.update(locators)

    def get_namespace_prefix(self, name):
        parts = name.split('__')
        if parts[-1] == 'c':
            parts = parts[:-1]
        if len(parts) > 1:
            return parts[0] + '__'
        else:
            return ''

    def get_npsp_namespace_prefix(self):
        if not hasattr(self.cumulusci, '_describe_result'):
            self.cumulusci._describe_result = self.cumulusci.sf.describe()
        objects = self.cumulusci._describe_result['sobjects']
        level_object = [o for o in objects if o['label'] == 'Level'][0]
        return self.get_namespace_prefix(level_object['name'])

    def populate_field_by_placeholder(self, loc, value):
        """ Populate field with Place Holder as a locator
            and actual value of the place holder.
        """
        xpath = npsp_lex_locators["placeholder"].format(loc)
        field = self.selenium.get_webelement(xpath)
#         self.salesforce._populate_field(xpath, value)
        
        field.send_keys(value)
        time.sleep(2)
# #         if loc == ("Search Contacts" or "Search Accounts"):
#         field.send_keys(Keys.ENTER)
# #             field.send_keys(Keys.ARROW_DOWN)
        field.send_keys(Keys.ENTER)
    
    def populate_campaign(self,loc,value):
        """This is a temporary keyword added to address difference in behaviour between summer19 and winter20 release"""
        self.populate_field_by_placeholder(loc, value)
        print(self.latest_api_version)       
        if self.latest_api_version == 47.0:
            self.selenium.click_link(value)
            

    def click_record_button(self, title):
        """ Pass title of the button to click the buttons on the records edit page. Usually save and cancel are the buttons seen.
        """
        locator = npsp_lex_locators['record']['button'].format(title)
        self.selenium.set_focus_to_element(locator)
        button = self.selenium.get_webelement(locator)
        button.click()
        time.sleep(5)
        
    def select_tab(self, title):
        """ Switch between different tabs on a record page like Related, Details, News, Activity and Chatter
            Pass title of the tab
        """
        tab_found = False
        locators = npsp_lex_locators["tabs"].values()
        for i in locators:
            locator = i.format(title)
            if self.check_if_element_exists(locator):
                buttons = self.selenium.get_webelements(locator)
                for button in buttons:
                    if button.is_displayed():
                        self.salesforce._focus(button)
                        button.click()
                        time.sleep(5)
                        tab_found = True
                        break

        assert tab_found, "tab not found"    
        
    def click_special_related_list_button(self, heading, button_title):
        """ To Click on a related list button which would open up a new lightning page rather than a modal.
            Pass the list name and button name"""
        self.salesforce.load_related_list(heading)
        b_found = False
        locator = npsp_lex_locators["record"]["related"]["button"].format(
            heading, button_title
        )
        buttons=self.selenium.get_webelements(locator)
        for button in buttons:
            if button.is_displayed():
                button.click()
                b_found = True
                break
            
        assert b_found, "{} related list with button {} not found.".format(heading, button_title)
                  
    def click_related_list_dd_button(self, heading, dd_title, button_title):
        """ To Click on a related list dropdown button.
            Pass the list name, dd name and button name"""
        self.salesforce.load_related_list(heading)
        locator = npsp_lex_locators["record"]["related"]["button"].format(heading, dd_title)
        self.selenium.click_link(locator) 
        time.sleep(1)
        loc=npsp_lex_locators["record"]["related"]["dd-link"].format(button_title)
        self.selenium.wait_until_element_is_visible(loc)
        self.selenium.click_link(loc)   
        
    def click_dropdown(self, title):
        """Click the dropdown to open it"""
        locator = npsp_lex_locators['record']['list'].format(title)
        self.selenium.set_focus_to_element(locator)
        self.selenium.get_webelement(locator).click()
        self.wait_for_locator('popup')
        
    def click_flexipage_dropdown(self, title):
        """Click the lightning dropdown to open it"""
        locator = npsp_lex_locators['record']['flexipage-list'].format(title)
        self.selenium.set_focus_to_element(locator)
        self.selenium.get_webelement(locator).click()
        self.wait_for_locator('flexipage-popup')    

    def open_date_picker(self, title):
        locator = npsp_lex_locators['record']['list'].format(title)
        self.selenium.set_focus_to_element(locator)
        self.selenium.get_webelement(locator).click()

    def pick_date(self, value):
        """To pick a date from the date picker"""
        locator = npsp_lex_locators['record']['datepicker'].format(value)
        self.selenium.set_focus_to_element(locator)
        self.selenium.get_webelement(locator).click() 

    def change_month(self, value):    
        """To pick month in the date picker"""
        locator = npsp_lex_locators['record']['month_pick'].format(value)
        self.selenium.set_focus_to_element(locator)
        self.selenium.get_webelement(locator).click()
        
#     def select_row(self,value):
#         """To select a row on object page based on name and open the dropdown"""    
#         drop_down = npsp_lex_locators['locating_delete_dropdown'].format(value)
#         self.selenium.get_webelement(drop_down).click()
#         #self.selenium.get_webelement(drop_down).click()

#     def select_row(self,value):
#         """To select a row on object page based on name and open the dropdown"""    
#         locator = npsp_lex_locators['select_name'].format(value)
#         self.selenium.set_focus_to_element(locator)
#         drop_down = npsp_lex_locators['locating_delete_dropdown'].format(value)
#         time.sleep(1)
#         return drop_down
    
    def select_row(self, value):
        """To select a row on object page based on name and open the dropdown"""
        locators = npsp_lex_locators['name']
        list_ele = self.selenium.get_webelements(locators)
        for index, element in enumerate(list_ele):
            if element.text == value:
                drop_down = npsp_lex_locators['locate_dropdown'].format(index + 1)
                self.selenium.get_webelement(drop_down).click()
                time.sleep(1)

    def select_related_row(self, value):
        """To select a row on object page based on name and open the dropdown"""
        locators = npsp_lex_locators['related_name']
        list_ele = self.selenium.get_webelements(locators)
        for index, element in enumerate(list_ele):
            if element.text == value:
                drop_down = npsp_lex_locators['rel_loc_dd'].format(index + 1)
                self.selenium.get_webelement(drop_down).click()
                time.sleep(1)
#     def select_row(self, value ):
#         """To select a row on object page based on name and open the dropdown"""
#         locators = npsp_lex_locators['name']
#         list_ele = self.selenium.get_webelements(locators)
#         index= 1
#         for locator in list_ele:
#             global index
#             if locator.text != value:
#                 index = index+1
#             else:
#                 drop_down = npsp_lex_locators['locate_dropdown'].format(index)
#                 self.selenium.get_webelement(drop_down).click()
#                 self.selenium.get_webelement(drop_down).click()
            
#     def select_related_row(self, value ):
#         """To select row from a related list based on name and open the dropdown"""
#         locators = npsp_lex_locators['related_name']
#         list_ele = self.selenium.get_webelements(locators)
#         index= 1
#         for locator in list_ele:
#             global index
#             if locator.text != value:
#                 index = index+1
#             else:
#                 drop_down = npsp_lex_locators['rel_loc_dd'].format(index)
#                 self.selenium.get_webelement(drop_down).click()
#                 self.selenium.get_webelement(drop_down).click()      
                
    def delete_icon(self, field_name,value):  
        """To click on x """
        locator=npsp_lex_locators['delete_icon'].format(field_name,value)
        self.selenium.get_webelement(locator).click() 

    def click_id(self, title):  
        locator=npsp_lex_locators['aff_id'].format(title)
        self.selenium.get_webelement(locator).click()     
         
    def select_object_dropdown(self): 
        locator=npsp_lex_locators['object_dd']
        self.selenium.get_webelement(locator).click()   
        
    def check_status(self, acc_name):
        aff_list = npsp_lex_locators['aff_status'].format(acc_name)
        aff_list_text=self.selenium.get_webelement(aff_list).text 
        self.aff_id=npsp_lex_locators['aff_id'].format(acc_name)
        self.aff_id_text=self.selenium.get_webelement(self.aff_id).text
        return self.aff_id_text,aff_list_text     
            
            
    def get_id(self):
        locator=npsp_lex_locators['click_aff_id'].format(self.aff_id_text)
        self.selenium.get_webelement(locator).click()   
        
        
    def confirm_value(self, field,value,status):
        list_found = False
        locators = npsp_lex_locators["confirm"].values()
        for i in locators:
            locator = i.format(field)
            if self.check_if_element_exists(locator):
                actual_value=self.selenium.get_webelement(locator).text
                if status.upper() == "Y":
                    assert value == actual_value, "Expected value to be {} but found {}".format(value, actual_value)
                elif status.upper() == "N":
                    assert value != actual_value, "Expected value {} and actual value {} should not match".format(value, actual_value)   
                list_found = True
                break

        assert list_found, "locator not found"  
 
            
    def verify_field_value(self, field,value,status):
        locator=npsp_lex_locators['check_field'].format(field)
        actual_value=self.selenium.get_webelement(locator).text
        if status.upper() == "Y":
            assert value == actual_value, "Expected value to be {} but found {}".format(
                value, actual_value
            )
        elif status.upper() == "N":
             assert value != actual_value, "Expected value {} and actual value {} should not match".format(
                value, actual_value
            )         
    
    
    def verify_record(self, name):
        """ Checks for the record in the object page and returns true if found else returns false
        """
        locator=npsp_lex_locators['account_list'].format(name)
        self.selenium.page_should_contain_element(locator)

            
    def select_option(self, name):  
        """selects various options in Contact>New opportunity page using name
        """
        locator=npsp_lex_locators['dd_options'].format(name)
        self.selenium.get_webelement(locator).click()
        
    def verify_related_list_items(self,list_name,value):
        """Verifies a specified related list has specified value(doesn't work if the list is in table format)"""
        locator=npsp_lex_locators['related_list_items'].format(list_name,value)
        self.selenium.page_should_contain_element(locator)
    
    def click_span_button(self,title):  
        """clicks on the button under span tag"""      
        locator=npsp_lex_locators['span_button'].format(title)
        self.selenium.get_webelement(locator).click()  
        
    def header_field_value(self,title,value):   
        """Validates if the specified header field has specified value"""   
        locator= npsp_lex_locators['header_field_value'].format(title,value)
        self.selenium.page_should_contain_element(locator)
        
    def verify_header(self,value):   
        """Validates header value"""   
        locator= npsp_lex_locators['header'].format(value)
        self.selenium.page_should_contain_element(locator)    
        
    def Verify_affiliated_contact(self,list_name,first_name,last_name, y):   
        """Validates if the affiliated contacts have the added contact details enter Y for positive case and N for negative case"""
        name = first_name + ' ' + last_name
        locator = self.salesforce.get_locator('record.related.link', list_name, name)
        if y.upper()=="Y":
            self.selenium.page_should_contain_element(locator)
        elif y.upper()=="N":
            self.selenium.page_should_not_contain_element(locator)
        
    def fill_address_form(self, **kwargs):
        """Validates if the affiliated contacts have the added contact details enter Y for positive case and N for negative case""" 
        for label, value in kwargs.items():
            locator= npsp_lex_locators['manage_hh_page']['address'].format(label,value)
            if label=="Street":
                locator = locator+"textarea"
                self.selenium.get_webelement(locator).send_keys(value)
            else:
                locator = locator+"input"
                self.selenium.get_webelement(locator).send_keys(value)
                
    def fill_bge_form(self, **kwargs):
        for label, value in kwargs.items():
            if label=="Batch Description" or label == "custom_textarea":
                locator= npsp_lex_locators['bge']['field-text'].format(label,value)
                self.selenium.click_element(locator)  
                self.salesforce._populate_field(locator, value)              

            else:
                locator= npsp_lex_locators['bge']['field-input'].format(label,value)
                self.selenium.click_element(locator)
                self.salesforce._populate_field(locator, value)
     
         
    def verify_details_address(self,field,npsp_street, npsp_city, npsp_country):   
        """Validates if the details page address field has specified value"""   
        locator= npsp_lex_locators['detail_page']['address'].format(field)
        street, city, country = self.selenium.get_webelements(locator)
        if street.text ==  npsp_street and city.text == npsp_city and country.text == npsp_country:
            return "pass"
        else:
            return "fail"
   
    def validate_checkbox(self,name,checkbox_title):   
        """validates all 3 checkboxes for contact on manage hh page and returns locator for the checkbox thats required"""   
          
        locator=npsp_lex_locators['manage_hh_page']['mhh_checkbox'].format(name,"fauxCBInformal")
        self.selenium.page_should_contain_element(locator)
        
        locator=npsp_lex_locators['manage_hh_page']['mhh_checkbox'].format(name,"fauxCBFormal")
        self.selenium.page_should_contain_element(locator)
        
        locator=npsp_lex_locators['manage_hh_page']['mhh_checkbox'].format(name,"fauxCBExName") 
        self.selenium.page_should_contain_element(locator)
        
        if checkbox_title == "Informal Greeting":
            locator=npsp_lex_locators['manage_hh_page']['mhh_checkbox'].format(name,"fauxCBInformal")
        elif checkbox_title == "Formal Greeting":
            locator=npsp_lex_locators['manage_hh_page']['mhh_checkbox'].format(name,"fauxCBFormal") 
        elif checkbox_title.capitalize() == "Household Name":
            locator=npsp_lex_locators['manage_hh_page']['mhh_checkbox'].format(name,"fauxCBExName")       
        return locator
    
    def check_field_value(self, title, value):
        """checks value of a field in details page(section without header)"""
        fv_found=False
        locators = npsp_lex_locators['detail_page']["field-value"].values()

        for i in locators:
            locator = i.format(title,value)
            if self.check_if_element_exists(locator):
                self.selenium.page_should_contain_element(locator)
                fv_found = True
                break

        assert fv_found, "{} with {} not found".format(title,value)
        
    def click_managehh_button(self,title):  
        """clicks on the new contact button on manage hh page"""      
        locator=npsp_lex_locators['manage_hh_page']['button'].format(title)
        self.selenium.get_webelement(locator).click()  
        
    def click_managehh_link(self,title):       
        locator=npsp_lex_locators['manage_hh_page']['address_link'].format(title)
        self.selenium.get_webelement(locator).click()      
    
    def select_lightning_checkbox(self,title):
        """Clicks on a checkbox using field name"""
        cb_found=False
        locators = npsp_lex_locators["checkbox"].values()

        for i in locators:
            locator = i.format(title)
            if self.check_if_element_exists(locator):
                self.selenium.get_webelement(locator).click()
                cb_found = True
                break

        assert cb_found, "Checkbox not found"
        
    def select_bge_checkbox(self,title):
        locator=npsp_lex_locators['bge']['checkbox'].format(title)
        self.selenium.get_webelement(locator).click()     
        
    def populate_modal_field(self, title, value):
        locator=npsp_lex_locators['modal_field'].format(title,value)
        self.salesforce._populate_field(locator, value)
    
    def populate_field_with_id(self,id,value):
        locator=npsp_lex_locators['id'].format(id)
        if value == 'null':
            field = self.selenium.get_webelement(locator)
            self.salesforce._clear(field)
        else :    
            self.salesforce._populate_field(locator, value)
        
    def verify_occurrence(self,title,value):
        locator=npsp_lex_locators['record']['related']['check_occurrence'].format(title,value)
        actual_value=self.selenium.get_webelement(locator).text
        exp_value="("+value+")"
        assert exp_value == actual_value, "Expected value to be {} but found {}".format(
            exp_value, actual_value
        )  
        
    def check_record_related_item(self,title,value):
        locator=npsp_lex_locators['record']['related']['item'].format(title,value)
        self.selenium.wait_until_page_contains_element(locator)
        actual_value=self.selenium.get_webelement(locator).text
        assert value == actual_value, "Expected value to be {} but found {}".format(
            value, actual_value
        )      
          
     
    def select_related_dropdown(self,title):
        """Clicks on the dropdown next to Related List"""
        locator=npsp_lex_locators['record']['related']['drop-down'].format(title)
        self.selenium.get_webelement(locator).click()   
        
    def get_header_date_value(self,title):   
        """Validates if the specified header field has specified value"""   
        locator= npsp_lex_locators['header_datepicker'].format(title)
        date=self.selenium.get_webelement(locator).text   
        return date 
        
    def get_main_header(self):
        header_found = False
        locators = npsp_lex_locators["main-header"].values()

        for locator in locators:
            if self.check_if_element_exists(locator):
                header = self.selenium.get_webelement(locator).text
                header_found = True
                return header

        assert header_found, "Header with the provided locator not found"
    
    def verify_contact_role(self,name,role):
        """verifies the contact role on opportunity page"""
        locator=npsp_lex_locators['opportunity']['contact_role'].format(name,role)
        self.selenium.page_should_contain_element(locator)  
        
    def select_relatedlist(self,title):
        """click on the related list to open it"""
        locator=npsp_lex_locators['record']['related']['title'].format(title)
        self.selenium.get_webelement(locator).click()  
        
    def verify_related_list_field_values(self, **kwargs):
        """verifies the values in the related list objects page""" 
        for name, value in kwargs.items():
            locator= npsp_lex_locators['record']['related']['field_value'].format(name,value)
            self.selenium.wait_until_page_contains_element(locator,error="Could not find the "+ name +" with value " + value + " on the page")
            
    def verify_related_object_field_values(self, rel_object,**kwargs):
        """verifies the specified field,value pairs in the related object page (table format)""" 
        self.salesforce.load_related_list(rel_object)
        self.select_relatedlist(rel_object)
        for name, value in kwargs.items():
            locator= npsp_lex_locators['object']['field-value'].format(name,value)
            self.selenium.wait_until_page_contains_element(locator,error="Could not find the "+ name +" with value " + value + " on the page")
    
    
    def page_contains_record(self,title):   
        """Validates if the specified record is present on the page"""   
        locator= npsp_lex_locators['object']['record'].format(title)
        self.selenium.page_should_not_contain_element(locator) 
             
                         
               
    def click_special_object_button(self, title):
        """Clicks a button in an object's actions but doesn't wait for a model to open"""
        locator = npsp_lex_locators['object']['button'].format(title)
        self.selenium.wait_until_element_is_visible(locator,error="Button "+ title +" not found on the page")
        self.selenium.get_webelement(locator).click()
        
    def click_eng_plan_dropdown(self, title):
        locator = npsp_lex_locators['engagement_plan']['dropdown'].format(title)
        self.selenium.set_focus_to_element(locator)
        self.selenium.get_webelement(locator).click()
        
    def select_eng_plan_checkbox(self,title):
        """"""
        if title=="Skip Weekends":
            locator=npsp_lex_locators['engagement_plan']['checkbox'].format("span",title)
            self.selenium.get_webelement(locator).click()
        else:
            locator=npsp_lex_locators['engagement_plan']['checkbox'].format("label",title)
            self.selenium.get_webelement(locator).click()
            
    def enter_eng_plan_values(self, name, value):
        """Enter values into corresponding fields in Engagement Plan Templet page"""
        locator = npsp_lex_locators['id'].format(name) 
        self.salesforce._populate_field(locator, value)
    
    

                
    def enter_task_id_and_subject(self, id, value):
        """Enter values into corresponding task subject fields based on last 2 digits of id"""
        locator = npsp_lex_locators['engagement_plan']['input_box'].format(id) 
        self.selenium.get_webelement(locator).send_keys(value)
    
    
    def click_task_button(self, task_id, name):
        """Click Task button based on Task id and button label"""          
        locator = npsp_lex_locators['engagement_plan']['button'].format(task_id, name)
        self.selenium.get_webelement(locator).click()    
          
    
    def check_related_list_values(self,list_name,*args):
        """Verifies the value of custom related list"""
        for value in args:
            locator = npsp_lex_locators['check_related_list_item'].format(list_name,value)
            self.selenium.page_should_contain_element(locator)

    def verify_eng_plan_exists(self,name, delete=None):  
        """verifies that the Engagement Plans related list has a plan stored under it and clicks on dropdown if True is passed as 2nd argument"""
        locator = npsp_lex_locators['engagement_plan']['check_eng_plan'].format(name)
        self.selenium.page_should_contain_element(locator) 
        plan=self.selenium.get_webelement(locator).text   
        if delete == "True":
               locator = npsp_lex_locators['engagement_plan']['dd'].format(name)
               self.selenium.get_webelement(locator).click()      
        return plan
    
    def check_activity_tasks(self, *args):
        """verifies that the specified tasks are present under activity tab """
        for value in args:
            locator = npsp_lex_locators['engagement_plan']['tasks'].format(value)
            self.selenium.page_should_contain_element(locator)

    def enter_level_values(self, **kwargs):
        """Enter values into corresponding fields in Levels page"""
        for name, value in kwargs.items():
            if name == "Level Name":
                id = "fldName"
                locator = npsp_lex_locators['levels']['id'].format(id)
                self.salesforce._populate_field(locator, value)      
            elif name == "Minimum Amount":
                id = "fldMinAmount"
                locator = npsp_lex_locators['levels']['id'].format(id)
                self.salesforce._populate_field(locator, value)  
            elif name == "Maximum Amount":
                id = "fldMaxAmount"
                locator = npsp_lex_locators['levels']['id'].format(id)
                self.salesforce._populate_field(locator, value)                    

    def enter_level_dd_values(self, name,value):
        """Enter values into corresponding fields in Levels page"""                 
        if name == "Target":
            id = "fldTarget"
            locator = npsp_lex_locators['levels']['select'].format(id)
            loc = self.selenium.get_webelement(locator)
            self.selenium.set_focus_to_element(locator)       
            self.selenium.select_from_list_by_label(loc,value)
            time.sleep(2)
        elif name == "Source Field":
            id = "fldSourceField"
            locator = npsp_lex_locators['levels']['select'].format(id)
            loc = self.selenium.get_webelement(locator) 
            self.selenium.set_focus_to_element(locator)      
            self.selenium.select_from_list_by_label(loc,value) 
            time.sleep(2) 
        elif name == "Level Field":
            id = "fldLevel"
            locator = npsp_lex_locators['levels']['select'].format(id)
            loc = self.selenium.get_webelement(locator) 
            self.selenium.set_focus_to_element(locator)      
            self.selenium.select_from_list_by_label(loc,value)
            time.sleep(2)
        elif name == "Previous Level Field":
            id = "fldPreviousLevel"
            locator = npsp_lex_locators['levels']['select'].format(id)
            loc = self.selenium.get_webelement(locator) 
            self.selenium.set_focus_to_element(locator)      
            self.selenium.select_from_list_by_label(loc,value) 

    def select_app_launcher_link(self,title):
        locator = npsp_lex_locators['app_launcher']['select-option'].format(title) 
        self.selenium.get_webelement(locator).click()
        time.sleep(1)
        
    def click_on_first_record(self):  
        """selects first record of the page"""
        locator = npsp_lex_locators['select_one_record']
        self.selenium.get_webelement(locator).click()
        time.sleep(1)  
        
    def select_search(self, index, value):
        """"""
        locator = npsp_lex_locators["click_search"].format(index)
        loc_value = self.selenium.get_webelement(locator).send_keys(value)
        loc = self.selenium.get_webelement(locator)
        #loc.send_keys(Keys.TAB+ Keys.RETURN)
        time.sleep(1)  
        
    def enter_gau(self, value):
        id = "lksrch"
        locator = npsp_lex_locators["id"].format(id)
        loc = self.selenium.get_webelement(locator)
        loc.send_keys(value)
        self.selenium.get_webelement("//*[@title='Go!']").click()
        time.sleep(1)

    def add_gau_allocation(self,field, value):
        locator = npsp_lex_locators["gaus"]["input_field"].format(field)
        self.salesforce._populate_field(locator,value)
            
        
    def click_save(self, page):
        if  page== "GAU":
            id="j_id0:theForm:j_id9:j_id10:saveBTN"
            locator = npsp_lex_locators["id"].format(id)
            self.selenium.get_webelement(locator).click()
     
    def enter_payment_schedule(self, *args):
        """Enter values into corresponding fields in Levels page"""                 
        #if name == "Payments":
        #id = ["paymentCount","intervals","intervalunits"]
        id = ["paymentCount","vfForm:intervalnumber","intervalunits"]
        for i in range(len(args)):
            locator = npsp_lex_locators['id'].format(id[i])
            loc = self.selenium.get_webelement(locator)
            self.selenium.set_focus_to_element(locator)       
            self.selenium.select_from_list_by_label(loc,args[i])
            time.sleep(2)    
                
    def verify_payment_split(self, amount, no_payments):
        loc = "//*[@id='pmtTable']/tbody/tr/td[2]/div//input[@value= '{}']"
        values = int(amount)/int(no_payments)
        #global self.val
        values_1 = "{:0.2f}".format(values)
        self.val = str(values_1)
        locator =  loc.format(self.val)
        list_payments = self.selenium.get_webelements(locator)
        self.t_loc=len(list_payments)
        if  self.t_loc == int(no_payments):
            for i in list_payments:
                self.selenium.page_should_contain_element(i)             
            return str(self.t_loc)
        else:
            return str(self.t_loc)
       
    def verify_date_split(self,date, no_payments, interval): 
        ddate=[]  
        mm, dd, yyyy = date.split("/")
        mm, dd, yyyy = int(mm), int(dd), int(yyyy)
        locator = npsp_lex_locators['payments']['date_loc'].format(date)
        t_dates = self.selenium.get_webelement(locator)
        self.selenium.page_should_contain_element(t_dates)
#            for i in range(int(no_payments) + 1):
        if mm <= 12:
            date_list = [mm, dd, yyyy]
            dates = list(map(str, date_list))
            new_date = "/".join(dates)
            mm = mm + int(interval)
            dates = list(map(str, date_list))
            #if new_date not in t_dates: 
            locator1 = npsp_lex_locators['payments']['date_loc'].format(new_date)
            t_dates = self.selenium.get_webelement(locator1)                  
            self.selenium.page_should_contain_element(t_dates)
        elif mm > 12:
            yyyy = yyyy + 1
            mm = (mm + int(interval))-(12+int(interval))
            #return "pass"
#         else:
#             return "fail"
        
    def click_viewall_related_list (self,title):  
        """clicks on the View All link under the Related List"""      
        locator=npsp_lex_locators['record']['related']['viewall'].format(title)
        self.selenium.get_webelement(locator).click()
        
    def click_button_with_value (self,title):  
        """clicks on the button on the payments page"""      
        locator=npsp_lex_locators['button'].format(title)
        self.selenium.get_webelement(locator).click()
        
         
    def verify_details(self, **kwargs):
       """To verify no. of records with given same column values
          key is value in a table column, value is expected count of rows with that value     
       """
       for key, value in kwargs.items():
           locators = npsp_lex_locators['payments']['pays'].format(key)
           list_ele = self.selenium.get_webelements(locators)
           p_count=len(list_ele)
           assert p_count == int(value), "Expected {} payment with status {} but found {}".format(value, key, p_count)  
           
           
    def verify_allocations(self,header, **kwargs):
       """To verify allocations, header is related list
          key is value in 1st td element, value is value in 2nd element     
       """
       self.salesforce.load_related_list(header)
       for key, value in kwargs.items():
           locator = npsp_lex_locators['record']['related']['allocations'].format(header,key,value)
           self.selenium.wait_until_page_contains_element(locator,error="Expected {} allocation of {} was not found".format(key,value))
#            ele = self.selenium.get_webelement(locator).text
#            assert ele == value, "Expected {} allocation to be {} but found {}".format(key,value,ele)                      
                
    def verify_occurrence_payments(self,title,value=None):
        """"""
        locator=npsp_lex_locators['payments']['check_occurrence'].format(title)
        occ_value=self.selenium.get_webelement(locator).text
        return occ_value        
        
        
    def verify_payment(self):
        locators=npsp_lex_locators['payments']['no_payments']
        list_ele=self.selenium.get_webelements(locators)
        l_no_payments = len(list_ele)
        #return list_ele
        #return l_no_payments, self.t_loc
        #if self.t_loc == l_no_payments:
        for element in list_ele:
            payment_com=self.selenium.get_webelement(element).text
            cc=payment_com.replace("$","")
            if cc == str(self.val) and self.t_loc == l_no_payments :
                return 'pass'
            #return cc, self.val
            else:
                return "fail"
        
    def select_value_from_list(self,list_name,value): 
        locator = npsp_lex_locators['npsp_settings']['list'].format(list_name)
        loc = self.selenium.get_webelement(locator)
        self.selenium.set_focus_to_element(locator)       
        self.selenium.select_from_list_by_label(loc,value) 
          
        
    def select_value_from_bge_dd(self, list_name,value):
        list_found = False
        locators = npsp_lex_locators["bge-lists"].values()

        for i in locators:
            locator = i.format(list_name)
            if self.check_if_element_exists(locator):
                loc=self.selenium.get_webelement(locator)
                self.selenium.set_focus_to_element(locator)       
                self.selenium.select_from_list_by_label(loc,value)
                list_found = True
                break

        assert list_found, "Dropdown with the provided locator not found"

    def check_if_element_exists(self, xpath):
        elements =self.selenium.get_element_count(xpath)
        return True if elements > 0 else False
    
    def select_multiple_values_from_list(self,list_name,*args): 
        """Pass the list name and values to be selected from the dropdown. Please note that this doesn't unselect the existing values"""
        locator = npsp_lex_locators['npsp_settings']['multi_list'].format(list_name)
        loc = self.selenium.get_webelement(locator)
        self.selenium.set_focus_to_element(locator)       
        self.selenium.select_from_list_by_label(loc,*args) 
        
    def choose_frame(self, value):
        """Returns the first displayed iframe on the page with the given name or title"""
        locator = npsp_lex_locators['frame_new'].format(value,value)
        frames = self.selenium.get_webelements(locator)
        for frame in frames:
            if frame.is_displayed():
                self.selenium.select_frame(frame)
                return frame
        raise Exception('unable to find visible iframe with title "{}"'.format(value))

    def select_frame_and_click_element(self,iframe,path, *args, **kwargs):
        """Selects the first displayed frame with given name or title and scrolls to element identified by locator and clicks """
        self.choose_frame(iframe)
        loc = self.get_npsp_locator(path, *args, **kwargs)
        self.selenium.wait_until_element_is_visible(loc, timeout=60)
        self.selenium.scroll_element_into_view(loc)
        self.selenium.click_element(loc)
        
        
    def get_npsp_locator(self, path, *args, **kwargs):
        """ Returns a rendered locator string from the npsp_lex_locators
            dictionary.  This can be useful if you want to use an element in
            a different way than the built in keywords allow.
        """ 
        locator = npsp_lex_locators
        for key in path.split('.'):
            locator = locator[key]
        main_loc = locator.format(*args, **kwargs)
        return main_loc   

    def wait_for_locator(self, path, *args, **kwargs):
        """Waits for 60 sec for the specified locator"""
        main_loc = self.get_npsp_locator(path,*args, **kwargs)    
        self.selenium.wait_until_element_is_visible(main_loc, timeout=90)
        
        
    def wait_for_batch_to_complete(self, path, *args, **kwargs):
        """Checks every 15 secs for upto 3.5mins for batch with given status
        """
        i = 0
        locator = self.get_npsp_locator(path,*args, **kwargs)
        while True:
            i += 1
            if i > 14:
                self.selenium.capture_page_screenshot()
                raise AssertionError(
                    "Timed out waiting for batch with locator {} to load.".format(locator)
                )
            else:    
                try:
                    self.selenium.wait_until_element_is_visible(locator)
                    break
                except Exception:
                    time.sleep(15)    

    def get_npsp_settings_value(self,field_name): 
        locator = npsp_lex_locators['npsp_settings']['field_value'].format(field_name)
        loc = self.selenium.get_webelement(locator).text  
        return loc 
    
    def click_panel_sub_link (self,title):  
        """clicks on the button on the payments page"""      
        locator=npsp_lex_locators['npsp_settings']['panel_sub_link'].format(title)
        self.selenium.get_webelement(locator).click()
     
    def click_settings_button (self,panel_id,btn_value):  
        """clicks on the buttons on npsp settings object using panel id and button value"""      
        locator=npsp_lex_locators['npsp_settings']['batch-button'].format(panel_id,btn_value)
        self.selenium.click_element(locator)   
        
 
    
    def verify_payment_details(self):
        locator = "//tbody/tr/td[2]/span/span"
        locs1 = self.selenium.get_webelements(locator)
        locator2 = "//tbody/tr/td[3]/span/span"
        locs2 = self.selenium.get_webelements(locator2)
        for i, j in list(zip(locs1, locs2)):
            #loc1_vaue = self.selenium.get_webelemt(i).text
            #loc2_vaue = self.selenium.get_webelemt(j).text
            if i.text == "Pledged" and j.text == "$100.00":
                pass
            else:
                return "fail"
        return len(locs1)

    # def verify_opportunities(self, len_value):
    #     locator = "//tbody/tr[12]/th"
    #     s = self.selenium.get_webelement(locator).text
    #     #return s
    #     strip_list = s.split(" ")
    #     date = strip_list[-1]
    #     date = date.split("/")
    #     date = list(map(int, date))
    #     mm, dd, yyyy = date
    #     for _ in range(int(len_value)):
    #         if mm == 12:
    #             mm = 1
    #             yyyy = yyyy + 1
    #             date = [mm, dd, yyyy]
    #             date = list(map(str, date))
    #             date = "/".join(date)
    #             loctor_contains = "//tbody//a[contains(@title , '{}')]".format(date)
    #             self.selenium.page_should_contain_element(loctor_contains)            
    #         else:
    #             mm = mm + 1
    #             date = [mm, dd, yyyy]
    #             date = list(map(str, date))
    #             date = "/".join(date)
    #             loctor_contains = "//tbody//a[contains(@title , '{}')]".format(date)
    #             self.selenium.page_should_contain_element(loctor_contains)

    def click_object_manager_button(self,title):  
        """clicks on the buttons in object manager"""      
        locator=npsp_lex_locators['object_manager']['button'].format(title)
        self.selenium.get_webelement(locator).click()  
        
    def click_bge_button(self,text):  
        """clicks on buttons for BGE"""  
        self.builtin.log("This test is using javascript to click on button as regular click wouldn't work with Summer19", "WARN")    
        locator=npsp_lex_locators['bge']['button'].format(text)
        self.selenium.set_focus_to_element(locator)
        time.sleep(1)
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.driver.execute_script('arguments[0].click()', element)
  
           
    
    def verify_title(self,title,value):
        """"""
        locator=npsp_lex_locators['bge']['title'].format(title,value)
        actual_value=self.selenium.get_webelement(locator).text
        assert value == actual_value, "Expected value to be {} but found {}".format(
            value, actual_value
        )             
    
    def page_scroll_to_locator(self, path, *args, **kwargs):
        locator = self.get_npsp_locator(path, *args, **kwargs)
        self.selenium.scroll_element_into_view(locator)   

    def get_bge_card_header(self,title):   
        """Validates if the specific header field has specified value"""   
        locator= npsp_lex_locators['bge']['card-header'].format(title)
        id=self.selenium.get_webelement(locator).text   
        return id    
        
    def click_bge_edit_button(self, title):  
        """clicks the button in the table by using name mentioned in data-label"""
        locator=npsp_lex_locators['bge']['edit_button'].format(title)
        #self.selenium.get_webelement(locator).click()
        self.selenium.click_button(locator)
            
    def populate_bge_edit_field(self, title, value):
        """Clears the data in input field and enters the value specified """
        locator=npsp_lex_locators['bge']['edit_field'].format(title)
        field=self.salesforce._populate_field(locator, value)
 
        
    def verify_row_count(self,value):
        """verifies if actual row count matches with expected value"""
        locator=npsp_lex_locators['bge']['count']
        actual_value=self.selenium.get_webelements(locator)
        count=len(actual_value)
        assert int(value) == count, "Expected rows to be {} but found {}".format(
            value, count
        )       
     
    def return_locator_value(self, path, *args, **kwargs): 
        """Returns the value pointed by the specified locator"""
        locator=self.get_npsp_locator(path, *args, **kwargs)
        value=self.selenium.get_webelement(locator).text   
        return value
        
    def return_list(self, path, *args, **kwargs): 
        """Returns all the values pointed by the specified locator"""
        locator=self.get_npsp_locator(path, *args, **kwargs)
        values=self.selenium.get_webelements(locator)
        return [i.text for i in values]

    def select_bge_row(self, value):
        """To select a row on object page based on name and open the dropdown"""
        locators = npsp_lex_locators['bge']['name']
        list_ele = self.selenium.get_webelements(locators)
        for index, element in enumerate(list_ele):
            if element.text == value:
                drop_down = npsp_lex_locators['bge']['locate_dropdown'].format(index+1)
                self.selenium.click_element(drop_down)
                time.sleep(1)

    def click_link_with_text(self, text):
        self.builtin.log("This test is using the 'Click link with text' workaround", "WARN")
        locator = npsp_lex_locators['link-text'].format(text)
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.driver.execute_script('arguments[0].click()', element)  
    
    def verify_expected_batch_values(self, batch_id,**kwargs):
        """To verify that the data in Data Import Batch matches expected value provide batch_id and the data u want to verify"""    
        ns=self.get_npsp_namespace_prefix()
        table=ns + "DataImportBatch__c"
        bge_batch=self.salesforce.salesforce_get(table,batch_id)
        for key, value in kwargs.items():
            label=ns + key
            self.builtin.should_be_equal_as_strings(bge_batch[label], value)
            
    def click_element_with_locator(self, path, *args, **kwargs):
        """Pass the locator and its values for the element you want to click """
        locator=self.get_npsp_locator(path, *args, **kwargs)  
        self.selenium.click_element(locator)      
            
    def wait_for_record_to_update(self, id, value):
        """Waits for specified record header to be updated by checking every second for 10 times.
        """
        i = 0
        while True:
            i += 1
            if i > 10:
                raise AssertionError(
                    "Timed out waiting for record name to be {} .".format(value)
                )
            self.salesforce.go_to_record_home(id)
            try:
                self.verify_header(value)
                break
            except Exception:
                time.sleep(1)
                     
    def load_locator(self, locator):
        """Scrolls down until the specified locator is found.
        """
        i = 0
        while True:
            i += 1
            if i > 20:
                raise AssertionError(
                    "Timed out waiting for locator {} to load.".format(locator)
                )
            self.selenium.execute_javascript("window.scrollBy(0, 100)")
            self.wait_for_aura()
            try:
                self.selenium.get_webelement(locator)
                break
            except ElementNotFound:
                time.sleep(0.2)
                        
    def select_multiple_values_from_duellist(self,path,list_name,section,*args): 
        """Pass the list name and values to be selected from the dropdown. """
        main_loc = npsp_lex_locators
        for key in path.split('.'):
            main_loc = main_loc[key]
        for i in args:
            locator = main_loc.format(list_name,section,i)
            if args.index(i)==0:
                self.selenium.click_element(locator)
            else:
                self.selenium.click_element(locator,'COMMAND')
                
    def click_duellist_button(self, list_name,button):
        list_found = False
        locators = npsp_lex_locators["bge-duellist-btn"].values()

        for i in locators:
            locator = i.format(list_name,button)
            if self.check_if_element_exists(locator):
                loc=self.selenium.get_webelement(locator)
                self.selenium.click_element(locator)
                list_found = True
                break

        assert list_found, "Dropdown with the provided locator not found"            
    
    def verify_expected_values(self,ns_ind,obj_api,rec_id,**kwargs):
       """To verify that the data in database table match with expected value, 
       provide ns if object has namespace prefix otherwise nonns,
       object api name, record_id and the data u want to verify"""    
       if(ns_ind=='ns'):
           ns=self.get_npsp_namespace_prefix()
           table=ns + obj_api
       else:
            table=obj_api
       rec=self.salesforce.salesforce_get(table,rec_id)
       for key, value in kwargs.items():
           self.builtin.should_be_equal_as_strings(rec[key], value)

    def get_org_namespace_prefix(self):
        if self.cumulusci.org.namespaced:
            return "npsp__" 
        else:
            return ""       
          
    def click_first_matching_related_item_popup_link(self,heading,rel_status,link):
        '''Clicks a link in the popup menu for first matching related list item.
        heading specifies the name of the list,
        rel_status specifies the status or other field vaule to identify a particular item,
        and link specifies the name of the link'''  
        self.salesforce.load_related_list(heading)
        locator = npsp_lex_locators["record"]["related"]["link"].format(heading, rel_status)
        list=self.selenium.get_webelements(locator)
        title=list[0].text
        self.salesforce.click_related_item_popup_link(heading, title, link)
        
    def verify_field_values(self,**kwargs):
        """Verifies values in the specified fields""" 
        for key, value in kwargs.items():
            locator=npsp_lex_locators["field-value"].format(key)
            res=self.selenium.get_webelement(locator).text
            assert value == res, "Expected {} value to be {} but found {}".format(key,value,res)
            
    def checkbox_status(self,cbx_name,status):
        """verifies if the specified checkbox is with expected status in readonly mode"""
        locator=npsp_lex_locators["custom_settings"]["cbx_status"].format(cbx_name,status)
        self.selenium.page_should_contain_element(locator)
                
    def go_to_setup_page(self,page):
        """ Navigates to the specified page in Salesforce Setup """
        url = self.cumulusci.org.lightning_base_url
        url = "{}/lightning/setup/{}/home".format(url,page)
        self.selenium.go_to(url)
        self.salesforce.wait_until_loading_is_complete()

    def click_wrapper_related_list_button(self,heading,button_title):  
        """Clicks a button in the heading of a related list when the related list is enclosed in wrapper.
           Waits for a modal to open after clicking the button.
        """  
        locator = npsp_lex_locators["record"]["related"]["button"].format(heading, button_title)
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.driver.execute_script('arguments[0].click()', element)   
        
    def change_view_to(self,view_name):
        """Changes the view on the object page to the selected view"""
        self.select_object_dropdown()
        locator=npsp_lex_locators['link'].format(view_name)
        self.selenium.click_element(locator)     
        
    def wait_until_url_contains(self,exp_text):
        """Waits for maximum of 90sec for current url to contain the exp_text"""
        self.builtin.log("This keyword can be removed once we support SeleniumLibrary 4.0.")
        url=self.selenium.get_location()
        i=0
        for i in range(10):
            if i == 9:
                raise AssertionError("Failed to find an url containing {} in 90 seconds".format(exp_text))
            if exp_text in url:
                break
            else:
                time.sleep(10)
                url=self.selenium.get_location()
                i += 1
