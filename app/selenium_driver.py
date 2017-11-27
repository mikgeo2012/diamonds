from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from singleton import singleton
from bs4 import BeautifulSoup
from enum import Enum

@singleton
class SeleniumDriver:
    username = "mikgeo2012@gmail.com"
    password = "Prabhu1309"

    _hcaurl = "https://www.pricescope.com/tools/hca"
    _loginurl = "https://www.pricescope.com/community/login"


    def __init__(self):
        self._driver = webdriver.PhantomJS()
        self._driver.get(self._loginurl)
        if self.loginForHCA():
            self._driver.get(self._hcaurl)
        else:
            self.close()
            print "ERROR: Selenium Driver was not able to start for HCA score..."


    def loginForHCA(self):
        username = self._driver.find_element_by_css_selector("input#ctrl_pageLogin_login")
        username.send_keys(self.username)
        password = self._driver.find_element_by_css_selector("input#ctrl_pageLogin_password")
        password.send_keys(self.password)
        self._driver.find_element_by_css_selector('[data-loginphrase="Log in"]').click()

        login_success = self._driver.find_element_by_css_selector("strong.accountUsername")

        if login_success:
            print "HCA Login Successful...."
            return True
        else:
            print "HCA Login Failed..."
            return False




    def findHCAScore(self, data):
        login_success = self._driver.find_element_by_css_selector("strong.accountUsername")

        if login_success:
            print "Logged into HCA"

            try:
                for k, v in data.iteritems():
                    element = self._driver.find_element_by_name(k)
                    if element.tag_name == "input":
                        element.clear()
                        element.send_keys(str(v))

                self._driver.find_element_by_css_selector('[value="Go"]').click()


                html = self._driver.page_source

                soup = BeautifulSoup(html, "html.parser")

                hca_score = soup.find("span", {"id": "newhca_rating"})
                return hca_score.text.strip()

                # div_content = soup.find_all('div', class_ = 'content-middle')

                # tr = div_content[0].find('tr', {'bgcolor': '#339966'}) if div_content[0].find('tr', {'bgcolor': '#339966'}) is not None else div_content[0].find('tr', {'bgcolor': '#00cc00'})

                # return tr.find_all('td')[1].text.split("-")[0].strip()
            except Exception:
                print "Error while finding HCA score"
                raise
        else:
            print "Not logged into HCA"
            raise



        # finally:
            # self._driver.quit()


    def close(self):
        self._driver.quit()




















