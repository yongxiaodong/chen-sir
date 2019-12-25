from selenium import webdriver
import time
import requests
import re
import tesserocr
from PIL import Image
import os
def get_code(domain_name):

    driver.get('http://www.beian.gov.cn/portal/registerSystemInfo')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="websites"]').send_keys(domain_name)
    img = driver.find_element_by_xpath('//*[@id="websitesform"]/div/div[2]/div/img')
    img.screenshot('./img/b.png')

def identification_code():
    allpic = os.listdir('./img')
    for i in allpic:
        i = os.path.join('./img',i)
        image = Image.open(f"{i}")
        #进行置灰处理
        image = image.convert('L')
        #这个是二值化阈值
        threshold = 150
        table = []

        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        #通过表格转换成二进制图片，1的作用是白色，不然就全部黑色了
        image = image.point(table,"1")
        # image.show()
        result = str(tesserocr.image_to_text(image)).strip()
        return result
def test_code(result):

    dd = re.findall('\w*-\w*-\w*-\w*-\w*', driver.page_source)
    o_cookie = driver.get_cookies()
    headers = {}
    headers['Cookie'] = f"{o_cookie[1]['name']}={o_cookie[1]['value']}; {o_cookie[0]['name']}={o_cookie[0]['value']}"
    data = {
        'token': dd[0]
    }

    url = f'http://www.beian.gov.cn/portal/verCode?t=1&code={result}'
    r2 = requests.post(url=url, data=data, headers=headers)
    if r2.text == '0':
        print(f'验证码测试失败,开始重新测试')
        return 0
    else:
        print(f'验证码测试正确')
        driver.find_element_by_xpath('//*[@id="ver3"]').send_keys(result)
    #   driver.find_element_by_xpath('//*[@id="websitesform"]/div/div[3]/div/button').click()
        return 1

if __name__ == '__main__':
    driver = webdriver.Chrome()
    domain_name = '90qj.com'
    while True:
        print(f'当前处理{domain_name}')
        get_code(domain_name)
        result = identification_code()
        r = test_code(result)
        if r == 1:
            break

