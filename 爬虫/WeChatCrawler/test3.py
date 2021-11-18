import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq
import pymongo
from config import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.PhantomJS(service_args=SERVICE_ARGS) # 必须为键值对形式,否则会报错
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)
# 判断该元素是否加载完成，等待的最长时间为十秒
def search():
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com/')
        input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))) #等待时间
        submit = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))

        input.send_keys('美食') # 关键词
        submit.click()
        total = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_product()
        return total.text
    except TimeoutException:
        return search()
    # 输入“美食”
    # WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
    # 程序每隔xx秒看一眼，如果条件成立了，则执行下一步，否则继续等待，直到超过设置的最长时间，然后抛出TimeoutException


def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        # 输入页码数

        submit = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        # 点击确定
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_product()
    # 执行翻页操作（判断当前的页码是不是翻到的页数）
    ##mainsrp-pager > div > div > div > ul > li.item.active > span
    # 判断是否为那一页
    except TimeoutException:
        # 出错了则重新执行这一次请求
        next_page(page_number)


def get_product():
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    try:
        if db[MONGGO_TABLE].insert(result):
            print('保存成功', result)
    except Exception:
        print('保存失败', result)


def main():
    total = search()
    # total=total.text
    total = int(re.compile('(\d+)').search(total).group(1))
    print(total)

    for i in range(2, total + 1):
        next_page(i)
    browser.close()


if __name__ == '__main__':
    main()