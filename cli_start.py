#!/usr/bin/env python

import re, sys
import web_scraper as webScr
import img_processor as imgPro
import requests
import os
import argparse
from diamond import Diamond
from database import DataBase as DB
import utils as ut
from selenium_driver import SeleniumDriver

DATA_STORE_FILE = 'data/datastore.csv'

db = DB()

def run():

    while True:
        try:
            url = raw_input("==> ")
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            sel_driver.close()
            raise SystemExit


        if url == "q":
            print("Goodbye!")
            sel_driver.close()
            sys.exit(0)

        try:
            if url == 'o':
                    data = db.returnAll()
                    ut.printToFile(data)
            elif url == 't':
                consumeURL("https://www.jamesallen.com/loose-diamonds/round-cut/1.13-carat-g-color-si1-clarity-excellent-cut-sku-2653518?a_aid=55f8cd4e21a11")
                print
            elif url == 'pr':
                # data = db.returnGood()
                data = db.returnSorted('di/crt')
                ut.printToConsole(data)
            else:
                print webScr.parseForAvailability(url)
                #consumeURL(url)
                print
        except Exception as e:
            print e
            sel_driver.close()


def consumeURL(url):
    if url not in db.returnUrls():
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
                webScr.parseForInfo(imgName.split(".")[0].strip(), certNum, url)
    else:
        print "Diamond already in database"

if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog='run.py')
    ap.add_argument("-d", "--datasource", required = True, help = "Submit URL's via the command line or via a text file", choices=['cli', 'file'])
    ap.add_argument("-r", "--refresh", required = False, help = "Refresh database for availability", action = 'store_true')
    ap.add_argument("-p", "--purge", required = False, help = "Delete all data on database", action = 'store_true')
    args = vars(ap.parse_args())

    if args["refresh"] == True:
        try:
            print("Refreshing database.........")
            db.refreshDB()
        except Exception as e:
            print "Problem refreshing"
            print e
        print "Database refreshed"

    if args["purge"] == True:
        try:
            print("Deleting database.........")
            db.clean()
        except Exception as e:
            print "Problem purging the database"
            print e
        print "Database deleted."

    print "\n=========================================\n"

    sel_driver = SeleniumDriver()

    if args["datasource"] == 'cli':
        print("Start entering your url's to save the GIA numbers. type 'q' to quit.")
        run()
    elif args["datasource"] == 'file':
        pth = raw_input("Put the file into the datasource folder and enter the name of the file ==> ")

        with open("data/datasource/" + pth, 'r') as f:
                for line in f:
                    consumeURL(line.strip())

        try:

            next_step = raw_input("Press o to print existing diamond data / d to add URL's via command line / q to quit ==> ")

            if next_step == 'o':
                data = db.returnSorted('di/crt')
                ut.printToFile(data)
            if next_step == 'd':
                print("Start entering your url's to save the GIA numbers. type 'q' to quit.")
                run()
            else:
                print("\nBye!")
                sel_driver.close()
                raise SystemExit
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            sel_driver.close()
            raise SystemExit







