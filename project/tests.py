# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# go to the google home page
driver.get("http://a64.isp.nsc.ru")

# the page is ajaxy so the title is originally this:
print driver.title

# find the element that's name attribute is q (the google search box)
#

driver.find_element_by_id("log-in").click()
WebDriverWait(driver, 10)

inputElement = driver.find_element_by_id("id_username")
inputElement.send_keys("admin")
inputElement = driver.find_element_by_id("id_password")
inputElement.send_keys("admin")
inputElement.submit()

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 10)
    #.until(EC.body_contains("Выйти"))
    result = driver.find_elements_by_xpath("//a[@href='/accounts/logout/']")
    # You should see "cheese! - Google Search"
    print 'ok!'


finally:
    driver.quit()