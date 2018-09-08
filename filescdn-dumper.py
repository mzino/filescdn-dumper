# Original code by /u/seffignoz
# https://www.reddit.com/r/opendirectories/comments/6vysrh/lots_of_italian_books_is_there_any_way_to/dm46nig/
#
# Plus a few tweaks by /u/toyg
# https://gist.github.com/toyg/09ef7acae2ee97c6fd4c5016ef4ab8e0
#
# Stripped down to only dump a list of links by me.
#
# This is a Python 2.7 script; you will also need Requests and BeautifulSoup. 
# If you have virtualenv installed:
# $> virtualenv env
# $> source env/bin/activate
# $> pip install requests beautifulsoup
# $> python filescdn-dumper.py https://filescdn.net/f/folderid [start_page] [end_page]

import requests
import sys
import os
import argparse
from BeautifulSoup import BeautifulSoup
import HTMLParser

def build_list(root, start, end): #,interval
    print "\n* Dumping links from page",start,"to page",end,"... *"
    while (start <= end):
        print "\n* Dumping page",start,"..."
        html = requests.get(root + "/" + str(start)).content
        soup = BeautifulSoup(html)
        divs = soup.findAll("div")
        for d in divs:
            if str(d.get("class")) == "text-semibold":
                name = d.findAll("a")[0].text
                name = HTMLParser.HTMLParser().unescape(name)
                link = "https:" + str(d.findAll("a")[0].get("href"))
                # print "{}\t{}".format(link, name.encode("utf-8", "mixed"))
                with open("dump_"+root[-12:]+".txt", "a") as textfile:
                    print >> textfile, "{}\t{}".format(link, name.encode("utf-8", "mixed"))
                # sleep(interval)
        start += 1

def main():
    parser = argparse.ArgumentParser(description="*** FILESCDN LINK DUMPER ***")
    parser.add_argument("url", metavar="url", type=str, help="FilesCDN folder complete url (e.g. 'https://filescdn.net/f/folderid', without the final '/')")
    parser.add_argument("start_page", metavar="start_page", type=int, help="Dump starting from this page")
    parser.add_argument("end_page", metavar="end_page", type=int, help="Dump until this page (included)")
    args = parser.parse_args()
    build_list(args.url, args.start_page, args.end_page) #,sleep_interval

if __name__ == "__main__":
    main()
