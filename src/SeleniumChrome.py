import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from ReadFile import ReadFile
from WriteFile import WriteFile
from LotteryData import LotteryData
from log import Log
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import configparser
import sys


class SeleniumChrome:
    def __init__(self):
        chrome_driver_path = os.path.join(os.path.abspath(
            os.path.dirname(sys.argv[0])), "chromedriver.exe")
        options = Options()
        options.add_argument("--headless")
        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait
        self.weite_file = WriteFile()
        self.read_file = ReadFile()
        self.log = Log()
        self.lottery_data_list = []
        self.client_max_issue = 0

    def load_data(self):
        try:
            self.log.write_log("爬蟲開始!")
            print("爬蟲開始!")
            file = self.read_file.read_txt_file()
            if file:
                self.client_max_issue = int(
                    max(file, key=lambda x: int(x["Issue"]))["Issue"])
            self.get_data()
            self.weite_file.write_data(self.lottery_data_list)
            self.log.write_log("更新" + str(len(self.lottery_data_list)) + "筆")
            print("更新" + str(len(self.lottery_data_list)) + "筆")
            self.log.write_log("爬蟲完成!")
            print("爬蟲完成!")
        except Exception as ex:
            self.log.write_log(str(ex))
        finally:
            self.driver.quit()

    def get_data(self):
        try:
            day_range = int(self.get_config_value("DayRange"))
            lottery_url = self.get_config_value(
                "LotteryUrl") or "http://lotto.arclink.com.tw/"

            date = datetime.now() + timedelta(days=day_range)
            if date.weekday() == 6:
                date -= timedelta(days=1)
            start_date = date.strftime("%Y-%m-%d")

            self.driver.get(lottery_url)
            self.wait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it("dynamicInfo"))
            self.driver.find_element(By.NAME, "userName").send_keys(
                self.get_config_value("UserId"))
            self.driver.find_element(By.NAME, "password").send_keys(
                self.get_config_value("UserPwd"))

            login_btn = self.wait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/form/table/tbody/tr/td[3]/input"))
            )
            login_btn.click()
            self.driver.switch_to.default_content()
            self.driver.get("http://lotto.arclink.com.tw/Lotto39List.html")
            self.wait(self.driver, 10)

            dropdown_start_name = "periods1"
            dropdown_start_date = self.wait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, dropdown_start_name))
            )
            select_element = Select(dropdown_start_date)
            select_element.select_by_visible_text(start_date)

            self.wait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "Submit"))
            ).click()

            issue_count = len(self.driver.find_elements(
                By.XPATH, "/html/body/table[3]/tbody/tr"))
            if issue_count == 0:
                self.wait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/table[3]/tbody/tr"))
                )
            self.lottery_data_list = []
            max_issue_xpath = f"//td[1][text() > '{
                self.client_max_issue}']/parent::tr"
            lottery_rows = self.driver.find_elements(By.XPATH, max_issue_xpath)
            for row in lottery_rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                lottery_data = LotteryData(
                    issue=columns[0].text,
                    lottery_date=columns[1].text,
                    numbers=columns[2].text
                )
                self.lottery_data_list.append(lottery_data)
        except Exception as ex:
            self.log.write_log(f"Get data error: {str(ex)}")

    def get_config_value(self, key):
        config = configparser.ConfigParser()

        try:
            # 使用絕對路徑以確保文件正確解析
            config.read(os.path.join(
                os.path.dirname(sys.argv[0]), 'config.ini'))
            return os.environ.get(key) or config.get('Settings', key, fallback="")
        except Exception as ex:
            # 讀取配置時發生錯誤
            print(f"Error reading configuration: {ex}")
            return ""
