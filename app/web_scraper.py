from bs4 import BeautifulSoup
import urllib
import requests
import re
import smtplib
import os
import uuid
# from diamond import Diamond

import urllib2
import itertools
import utils
from decimal import *

# from database import DataBase as DB


imgPath = "images/original"
TABLE_INDEX = {'spec5': 'shape','spec6': 'color','spec7': 'cut','spec8': 'carat','spec9': 'clarity','spec14': 'depth', 'spec15': 'table', 'spec18': 'culet', 'spec32': ('crown', 'pavilion'), 'spec19': 'dim'}

# db = DB()

def parseForImage(url):
    try:

        req = requests.get(url)
        req.raise_for_status()

        soup = BeautifulSoup(req.text, "html.parser")

        a = soup.find("a", id="certificateIcon")
        imgUrl = a["certimg"]
        fileExt = os.path.basename(imgUrl).split(".")[-1]

        imgName = str(uuid.uuid1()).replace("-", "_")

        try:
            urllib.urlretrieve(imgUrl, os.path.abspath(
                imgPath) + "/" + os.path.basename(imgName) + ".{0}".format(fileExt))
        except IOError:
            print("File doesn't exist")
            raise
        except Exception as e:
            print(e)
            raise
        else:
            # filename = "datastore.csv"
            # append_write = 'a' if os.path.exists(filename) else 'w'

            # with open(filename, append_write) as f:
            #     f.write("{0} | {1}\n".format(str(imgName), str(url)))

            return imgName + ".{0}".format(fileExt)

    except requests.exceptions.RequestException as e:
        print(e)
        raise

def parseForInfo(uuid, certNum, url):

    try:
        print("Analyzing and creating Diamond....")
        req = requests.get(url)
        req.raise_for_status()

        soup = BeautifulSoup(req.text, "html.parser")
        attributes = {}

        try:
            for k, v in TABLE_INDEX.iteritems():

                if v.__class__ == tuple:
                    tr_elems = soup.find_all("tr", help=k)
                    td = {v[i]: tr_elems[i].find("span", id = "ItemValue").string for i in range(len(tr_elems)) if v[i] == tr_elems[i].find("span", id = "ItemName").string.split(" ")[0].strip()}
                    attributes.update(td)
                else:
                    attributes[v] = soup.find("tr", help=k).find("span", id = "ItemValue").string

                    if v == 'culet' and attributes[v] == 'None':
                        attributes[v] = str(0)


            attributes['price'] = str((soup.find("div", id="Price").span.find("meta", itemprop="price")["content"]))
            attributes['gia_num'] = certNum
            attributes['url'] = str(url)

            attributes['cut_score'] = parseForCutScore(certNum)
            attributes['hca_score'] = utils.HCAScore(attributes['depth'], attributes['table'], attributes['crown'], attributes['pavilion'], attributes['culet'])

            xy = attributes['dim'].split('*')[0:2]
            attributes['diameter'] = str((Decimal(xy[0]).quantize(Decimal('0.01')) + Decimal(xy[1]).quantize(Decimal('0.01'))) / Decimal('2.00'))

            # attributes['di_crt'] = (str((float(attributes['diameter']) - 6.5)/0.5), str((float(attributes['carat']) - 1.0)/0.25))

            dia_ratio = (float(attributes['diameter']) - 6.5)/0.5
            carat_ratio = (float(attributes['carat']) - 1.0)/0.25
            attributes['dia_carat'] = dia_ratio - carat_ratio

        except Exception:
            print "Diamond wasn't created"
            raise

        if float(attributes['cut_score']) >= 87 and float(attributes['hca_score']) <= 2:
            return attributes
        else:
            print "{0}   {1}   {2}".format(attributes['cut_score'], attributes['hca_score'], attributes['url'])
            return False


    except requests.exceptions.RequestException as e:
        print(e)
        raise

def parseForCutScore(gia_num):
    url = "https://enchanteddiamonds.com/cut-score-calculator?certificate="
    print "Getting cut score for: {0}.....".format(gia_num)
    try:

        req = requests.get(url + gia_num)
        req.raise_for_status()

        soup = BeautifulSoup(req.text, "html.parser")

        score = soup.find("div", "cut-score-calc-score").span.string

        return score

    except (requests.exceptions.RequestException, AttributeError) as e:
        print "GIA number might be translated incorrectly"
        print(e)
        raise


def parseForAvailability(url):
    try:

        req = requests.get(url)
        req.raise_for_status()

        soup = BeautifulSoup(req.text, "html.parser")

        avail = str((soup.find("div", id="Price").span.find("span", itemprop="availability")["content"]))

        if avail == 'Out of stock':
            return False
        else:
            return True
    except Exception as e:
        print e
        raise


def _testParser():
    self.parseForImage(
        "https://www.jamesallen.com/loose-diamonds/round-cut/1.27-carat-h-color-si1-clarity-excellent-cut-sku-3321702?a_aid=55f8cd4e21a11")
