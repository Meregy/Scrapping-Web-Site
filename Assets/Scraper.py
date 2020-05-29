import os
import fnmatch
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep


class Scrapping():
    def __init__(self, building_name):

        self.download_path = os.path.join(os.getcwd(), "data")
        self.url = "https://smart-villages.fsicloud.me/Evolution/!System/Tasks/F_TASKS/ViewF_TASKSItems.aspx"
        self.user_name = "Mohamed Meregy"
        self.password = '123456'
        self.building_URL = "//input[@name='ctl00$contentPlaceHolder$fsiGridTasks$innerGrid$ctl00$ctl02$ctl02$ctl03$listF_TASKS_TA_FKEY_BG_SEQ_BG_SITE_10']"
        self.chrome_path = os.path.join(os.getcwd(), os.path.join("Assets", "chromedriver.exe"))
        self.open_chrome(self.chrome_path, self.url)
        self.loggin_in(self.user_name, self.password)
        self.building_filter(self.building_URL, building_name)

    def open_chrome(self, chrome_path, url):
        self.prefer_ = {'download.default_directory': self.download_path,
                        'profile.default_content_settings.popups': 0,
                        'directory_upgrade': True}
        self.chrom_options_ = webdriver.ChromeOptions()
        self.chrom_options_.add_experimental_option('prefs', self.prefer_)
        self.driver = webdriver.Chrome(
            chrome_path,
            options=self.chrom_options_)

        self.driver.get(url)

    # ...............................Logging in ....................................
    def loggin_in(self, user_name, password):

        self.UsernameURL = "//input[@id='ctl00_contentPlaceHolder_loginControl_UserName']"
        self.PasswordURL = "//input[@id='ctl00_contentPlaceHolder_loginControl_Password']"
        self.ButtonURL = "//input[@id='ctl00_contentPlaceHolder_loginControl_LoginButton']"

        self.UserElement = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(self.UsernameURL))
        self.UserElement.send_keys(user_name)

        self.PasswordElement = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(self.PasswordURL))
        self.PasswordElement.send_keys(password)
        self.ButtonElement = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(self.ButtonURL))
        self.ButtonElement.click()

    # ...............................Filltering Building....................................
    # buildings = ["B104", "Oracle","B106","Arab Bank","B108-A" , "Talal Abo Ghazala","B109", "SV School","HERMES","B129","IBM","B144","B149","Smart School 01","B150","Pavilion","B19" , "SVC","B2111" , "Concordia","B217" , "National Investment Bank","B221 ", "FAWRY", "B2215" , "HUAWEI","B2401" , "Arab Academy","B3401" ," Dar El Handasa", "B69" , "Conference Center","B76" , "Smart Club","B79","Think tank","B81","Microsoft","B82" , "E-Finance","B86" , "ADCOM",]
    # buildings_lower = []
    # for building in buildings:
    #     buildings_lower.append(building.lower())
    # building_name = input("please Enter the Building Number Or Name: ")
    # while building_name.lower() not in buildings_lower:
    #     print("Please enter a valid Building Name or Building Number")
    #     building_name = input("please Enter the Building Number Or Name: ")
    # ...............................Inputs to Web Page ....................................
    def building_filter(self, building_URL, building_name):

        self.building_element = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(building_URL))
        self.building_element.clear()
        self.building_element.send_keys("*" + building_name)

        self.task_id_URL = "//input[@name='ctl00$contentPlaceHolder$fsiGridTasks$innerGrid$ctl00$ctl02$ctl02$ctl01$listF_TASKS_TA_TASK_ID_8']"
        self.task_id_element = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(self.task_id_URL))
        self.task_id_element.clear()

        self.refresh_URL = "//div[@class='toolbarContainer']//div[5]"
        self.refresh_element = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(self.refresh_URL))
        self.refresh_element.click()

    # ...............................find the latest file befor Downloading....................................
    def find_(self, pattern, path):
        self.result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                # if self.result:
                #     os.remove(os.path.join(root, name))
                if fnmatch.fnmatch(name, pattern):
                    self.result.append(os.path.join(root, name))
        return self.result

    def downloader(self):

        self.old_results = self.find_('Export*.csv', self.download_path)
        if not self.old_results:
            self.old_file = ""
        else:
            self.old_file = max(self.old_results, key=os.path.getctime)

        # ...............................Download CSV File....................................

        # self.save_URL = "//div[@class='saveButtonGridFooter']"
        # self.save_element = WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_xpath(self.save_URL))
        # self.save_element.click()

        self.download_URL = "//body/form[@name='aspnetForm']/div[@class='layoutTableContainer']/div/div/div/div/table[@class='RadSplitter RadSplitter_Default']/tbody/tr/td[@class='rspPane rspLastItem']/div/div/div[@class='contentWrapperPane']/div[@class='contentWrapperPaneStrip']/div[@class='innerLayoutContainer']/div[@class='fullSizeUpdatePanel']/div[@class='RadMultiPage RadMultiPage_Metro']/div[@class='rmpView']/div[@class='content contentInner']/div/div[@class='contentPlaceHolderPositioner']/div[@class='contentPlaceHolderWithTop']/div[@class='tasksLayoutContainer']/div[@class='tasksGridPanel ShowGridFilterPanel']/div/span[contains(@class,'interactiveModeContainer')]/div/div[@class='gridFillLayoutPanel']/div/div[@class='RadGrid RadGrid_Metro']/table[@class='rgMasterTable rgClipCells']/tbody/tr[contains(@class,'rgPager')]/td/span/span[@class='PagerActionPanel']/a[1]"
        self.download_element = WebDriverWait(self.driver, 25).until(
            lambda driver: self.driver.find_element_by_xpath(self.download_URL))
        self.download_element.click()

        # ...............................Open the latest CSV File....................................
        self.timeout = 0
        if not self.old_results:
            self.newest_file = self.find_('Export*.csv', self.download_path)
        else:
            while self.old_file == max(self.find_('Export*.csv', self.download_path), key=os.path.getctime):
                sleep(1)
                self.timeout += 1
                if self.timeout == 120:
                    raise TimeoutError("No New File downloaded")
            else:
                self.newest_file = max(self.find_('Export*.csv', self.download_path), key=os.path.getctime)
        return self.newest_file

    # # ...............................Logging out....................................
    def logging_out(self):
        self.User_click_URL = "//div[@class='badgeInitials']"
        self.User_click_elem = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(self.User_click_URL))
        self.User_click_elem.click()
        self.LogOut_URL = "//a[contains(text(),'Log Out')]"
        self.LogOut_elem = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(self.LogOut_URL))
        self.LogOut_elem.click()
        self.driver.quit()


