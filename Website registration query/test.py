from selenium import webdriver

import time
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome()
# driver.get('http://www.baidu.com')
# driver.get('http://www.so.com')
# driver.find_element_by_xpath('//*[@id="kw"]').send_keys('site:itgod.org')
# driver.find_element_by_xpath('//*[@id="su"]').click()
# time.sleep(2)
# # driver.implicitly_wait(5)
# print(driver.page_source)


with open('./domain_list','r') as f:
    print(len(f.readlines()))
    f.seek(0)
    for i in f:
        print(i)