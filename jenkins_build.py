from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("driver/chromedriver")
driver.get("http://anamika.englab.juniper.net:8080/job/Nuthan_contrail_command/build?delay=0sec")
driver.set_page_load_timeout(20)
driver.find_element_by_xpath("//button[text()='Build']").send_keys(Keys.ENTER)
time.sleep(2)
driver.find_element_by_xpath("//td[text()='User:']/following::td/input").send_keys("builder")
driver.find_element_by_xpath("//td[text()='Password:']/following::td/input").send_keys("builder@123")
driver.find_element_by_xpath("//button[text()='log in']").send_keys(Keys.ENTER)
time.sleep(2)
driver.find_element_by_xpath("//button[text()='Build']").send_keys(Keys.ENTER)

