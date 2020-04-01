from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import requests
import re
import tesserocr
from PIL import Image
import os
def write_info(info):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(info)
        f.write('------------------------------------------'+'\n')

def get_code(domain_name):
    driver.find_element_by_xpath('//*[@id="myTab"]/li[2]/a').click()
    driver.find_element_by_xpath('//*[@id="domain"]').send_keys(domain_name)
    img = driver.find_element_by_xpath('//*[@id="domainform"]/div/div[2]/div/img')
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
def test_code(result, domain_name):

    dd = re.findall('\w*-\w*-\w*-\w*-\w*', driver.page_source)
    o_cookie = driver.get_cookies()
    headers = {}
    headers['Cookie'] = f"{o_cookie[1]['name']}={o_cookie[1]['value']}; {o_cookie[0]['name']}={o_cookie[0]['value']}"
    data = {
        'token': dd[0]
    }

    url = f'http://www.beian.gov.cn/portal/verCode?t=2&code={result}'
    r2 = requests.post(url=url, data=data, headers=headers)
    if r2.text == '0':
        print(f'验证码测试失败,开始重新测试')
        return 0
    else:
        print(f'验证码测试正确')
        driver.find_element_by_xpath('//*[@id="ver2"]').send_keys(result)
        driver.find_element_by_xpath('//*[@id="domainform"]/div/div[3]/div/button').click()
        time.sleep(1)
        try:
            owner_name = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[3]/div[2]/table/tbody/tr[1]/td[2]').text
            record_code = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[3]/div[2]/table/tbody/tr[2]/td[2]').text
            record_zone = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[3]/div[2]/table/tbody/tr[3]/td[2]').text
            record_time = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[3]/div[2]/table/tbody/tr[4]/td[2]').text
            info = f'''
            域名: {domain_name}
            开办者名称: {owner_name}
            公安备案号: {record_code}
            备案地公安机关: {record_zone}
            联网备案时间: {record_time}
            '''
            print(info)
            write_info(info)
        except NoSuchElementException:
            info = f'''
            域名： {domain_name}
            公安备案号： 该网站无备案
            '''
            print(info)
            write_info(info)
        except Exception:
            info = f'''
            域名: {domain_name}
            公安备案号：查询时发生了未知错误
            '''
            print(info)
            write_info(info)
        finally:
            return 1

if __name__ == '__main__':
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    with open('./domain_list', 'r', encoding='utf-8') as f:
        list_count = len(f.readlines())
        f.seek(0)
        idx = 1
        for domain_name in f:
            domain_name = domain_name.strip().strip('\n')
            while True:
                print(f'当前处理{domain_name},当前处理第{idx}条,共计{list_count}条')
                driver.get('http://www.beian.gov.cn/portal/registerSystemInfo')
                get_code(domain_name)
                result = identification_code()
                r = test_code(result, domain_name)
                if r == 1:
                    break
            idx += 1
    driver.quit()
