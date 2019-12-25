from selenium import webdriver

# import time
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Chrome()
# driver.get('http://www.baidu.com')
# driver.find_element_by_xpath('//*[@id="kw"]').send_keys('site:itgod.org')
# driver.find_element_by_xpath('//*[@id="su"]').click()
# time.sleep(5)
# # driver.implicitly_wait(5)
# print(driver.page_source)


c = [{'domain': 'www.beian.gov.cn', 'httpOnly': False, 'name': 'BIGipServerPOOL-WebAGPT', 'path': '/', 'secure': False,
      'value': '202576044.37151.0000'},
     {'domain': 'www.beian.gov.cn', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/', 'secure': False,
      'value': '5B3F80687AA70761E060BF95E5473414'}]

a = '''<script type="text/javascript">
	var taken_for_user = 'fc4b14f6-c034-4448-b4c0-f7d503fbbdfe';
	</script>'''

import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
header['cookie'] = '''JSESSIONID=E568FA3C724B56CD0246B9C390D89751; BIGipServerPOOL-WebAGPT=185798828.37151.0000'''
data = {
    'token': 'd7efa966-6c55-4ca8-8b24-c3d849dc15a7'
}
print(header)
print(data)
print(f'http://www.beian.gov.cn/portal/verCode?t=1&code=3661')
r2 = requests.post(f'http://www.beian.gov.cn/portal/verCode?t=1&code=2766', data=data, headers=header)
print(r2.text, type(r2.text))

