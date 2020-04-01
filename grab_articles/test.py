import requests
from lxml import etree
import time


def parse_html(url):
    home_page_source = requests.get(url).text.encode('gbk','ignore').decode('gbk','ignore')
    # print(home_page_source)
    html = etree.HTML(home_page_source)
    return html


def get_home_data(html):
    # result = etree.tostring(html,encoding="gbk", pretty_print=True, method="html").decode('gbk')
    article_name_list = html.xpath('/html/body/section/div[1]/div/article/header/h2/a/text()')
    article_name_ref  = html.xpath('/html/body/section/div[1]/div/article/header/h2/a/@href')
    # for url in article_name_ref:
    #     get_article_page(url)
    get_article_page(article_name_ref[0])

def get_article_page(url):
    html = parse_html(url)
    result = etree.tostring(html, encoding="gbk", pretty_print=True, method="html").decode('gbk')
    print(result)
    content = html.xpath('/html/body/section/div[1]/div/article/text()')
    print(content)




if __name__ == '__main__':
    url = 'https://news.west.cn/topics/pm?tdsourcetag=s_pctim_aiomsg'
    html = parse_html(url)
    get_home_data(html)

