import requests


r = requests.get('http://www.beian.gov.cn/common/image.jsp?t=2')
for i in range(10):
    with open(f'./img/{i}.jpg', 'wb') as file:
        file.write(r.content)