import requests
import json
from bs4 import BeautifulSoup
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium_driver import SeleniumDriver
import os
import re, sys
import web_scraper as webScr
import img_processor as imgPro
from models import Diamond
from app import app, db



DATA_STORE_FILE = 'data/datastore.csv'
sel_driver = SeleniumDriver()

def HCAScore(depth, table, crown, pavilion, cutlet):
    data = {'depth_textbox': depth, 'table_textbox': table,
            'crown_listbox': 0, 'crown_textbox': crown, 'pavilion_listbox': 0, 'pavilion_textbox': pavilion, 'cutlet_textbox': cutlet}

    try:
        print "Getting HCA score....."

        return sel_driver.findHCAScore(data)
    except Exception:
        print "Couldn't find HCA Score"
        raise


def printToFile(d):
        filename = DATA_STORE_FILE

        with open(filename, 'w') as f:
            for di in d:
                f.write("{0} | {1} | {2} | {3} | {4} | {5} | {6}\n\n".format(str('$' + di['price']), di['carat'], di['cut_score'], di['hca_score'], di['diameter'], di['di/crt'], str(di['url'])))


def printToConsole(d):
    print "{0} | {1} | {2} | {3} | {4} | {5} | {6}\n".format('Price', 'Carat', 'Cut Score', 'HCA Score', 'Diameter', 'Diameter - Carat', 'URL')
    for di in d:
        print "{0} | {1} | {2} | {3} | {4} | {5} | {6}\n\n".format(str('$' + di['price']), di['carat'], di['cut_score'], di['hca_score'], di['diameter'], di['di/crt'], str(di['url']))

def consumeURL(url):
    diamonds = Diamond.query.filter_by(url=url).all()
    print str(len(diamonds)) + " if > 0 then duplicates exist"
    if len(diamonds) == 0:
        try:
            print("Downloading certificate....")
            imgName = webScr.parseForImage(url)

            print("Getting GIA number....")
            certNum = imgPro.analyze(imgName)

        except requests.exceptions.RequestException as reqEx:
            print("Couldn't download certificate. Try another url")
            print(reqEx)
            pass
        except IOError as ioerr:
            print("Couldn't find or read the file")
            print(ioerr)
        except Exception as e:
            print(e)
        else:
            if certNum:
                try:
                    return webScr.parseForInfo(imgName.split(".")[0].strip(), certNum, url)
                except Exception:
                    print "Couldn't read {0}".format(url)
                    pass
    else:
        pass

def refreshTable(urls):
    result = {}
    for k, v in urls.iteritems():
        try:
            if webScr.parseForAvailability(v.strip()):
                result.update(k = True)
            else:
                print str(k) + " is out of stock...."
                result.update(k = False)
        except Exception as e:
            print e
            raise
    return result

def deleteRow(id):
    try:
        diamond = Diamond.query.get(id)
        db.session.delete(diamond)
        db.session.commit()
    except Exception as e:
        print e
        raise

def deleteTable():
    try:
        db.session.query(Diamond).delete()
        db.session.commit()
    except:
        db.session.rollback()