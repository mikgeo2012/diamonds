from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from singleton import singleton
from bs4 import BeautifulSoup

@singleton
class SeleniumDriver:

    _url = "https://www.pricescope.com/tools/hca"


    def __init__(self):
        self._driver = webdriver.PhantomJS()
        self._driver.get(self._url)


    def findHCAScore(self, data):
        try:
            for k, v in data.iteritems():
                element = self._driver.find_element_by_name(k)
                if element.tag_name == "input":
                    element.clear()
                    element.send_keys(str(v))

            self._driver.find_element_by_css_selector("input#edit-send-quote1").click()


            html = self._driver.page_source

            soup = BeautifulSoup(html, "html.parser")

            div_content = soup.find_all('div', class_ = 'content-middle')

            tr = div_content[0].find('tr', {'bgcolor': '#339966'}) if div_content[0].find('tr', {'bgcolor': '#339966'}) is not None else div_content[0].find('tr', {'bgcolor': '#00cc00'})

            return tr.find_all('td')[1].text.split("-")[0].strip()
        except Exception:
            print "Error while finding HCA score"
            raise
        # finally:
            # self._driver.quit()


    def close(self):
        self._driver.quit()




















