from selenium import webdriver
from bs4 import BeautifulSoup
import time

class MainCrawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome('./browser/chromedriver', chrome_options=options)

    def run_companyToHome(self):
        self.driver.get('http://bus.go.kr/searchResult6.jsp')
        self.driver.find_element_by_id('searchname').send_keys('23202')
        self.driver.find_element_by_xpath('//*[@id="left"]/div[1]/div/span').click()

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        msg1 = soup.select('div.search_result_list_wrap > div > table > tbody > tr')[2].select('td.stat_arr > div')[1].text.strip()
        msg2 = soup.select('div.search_result_list_wrap > div > table > tbody > tr')[2].select('td.stat_arr > div')[3].text.strip()
        return {"res1":msg1, "res2":msg2}

    def run_rippleRealtimePrice(self):
        self.driver.get('https://www.clien.net/service/board/cm_vcoin')
        self.driver.find_element_by_xpath('//*[@id="XRP"]').click()
        time.sleep(0.1)
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        msg = soup.select('#coin_row_5 > span.board_krw.list > span')[0].text.strip()
        return msg