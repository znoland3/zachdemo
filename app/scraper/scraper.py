from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import flash, redirect, url_for
from ..models import ScrapeCount
from sqlalchemy.sql import func
from .. import db
import json
from ..main import errors
import sys
import re


# Main Scraper Class
class Scraper:

    def __init__(self, website):
        if website and self.validate_website(website):
            self._soup = ""
            self._elements = ""
            self._ElementUniqueList = []
            self._ElementList = []
            self._ElementDict = {}

            # Save Shortened Website Name
            self._ElementDict['websiteName'] = self.truncate_website(website)

            # Get Website Data
            html = urlopen(website)
            self._soup = BeautifulSoup(html)
            self._elements = self._soup.find_all()


        else:
            flash("the website could not be found")
            redirect(url_for('.index'))

    def validate_website(self, website):
        pass # Can add additional validation here
        return True

    def scrape(self):
        # Capture Total Count
        self._ElementDict['totalCount'] = self._elements.__len__()

        # Get unique list of elements
        for e in self._elements:
            if e.name not in self._ElementUniqueList:
                self._ElementUniqueList.append(e.name)

        # Capture unique count of elements
        self._ElementDict['uniqueCount'] = self._ElementUniqueList.__len__()

        # Create list
        self.create_element_list()

        # Get Historical Average
        self.get_average()

        # Insert to DB
        if self._ElementDict['websiteName'] != "google.com":
            self.db_insert()


        return self._ElementDict

    def create_element_list(self):
        # Creation list of Dictionaries
        for e in self._ElementUniqueList:
            self._ElementList.append({'name':e,
                                      'count':len(self._soup.find_all(e)),
                                      'details':[self.truncate_details(v) for v in self._soup.find_all(e)]})

        # Sort
        self._ElementList = sorted(self._ElementList, key=lambda k: k['count'], reverse=True)
        self._ElementDict['list'] = self._ElementList

    def truncate_details(self, v):
        if len(v.text) > 30:
            return v.text[:30] + '..'
        elif v.text == "":
            return "None"
        else:
            return v.text

    def truncate_website(self, v):
        v = re.match(r'https://www\.(.*)', v).group(1)
        if len(v) > 15:
            return v[:15] + '..'
        else:
            return v

    def db_insert(self):
        entry = ScrapeCount(websitename=self._ElementDict['websiteName'],
                            count=self._ElementDict['totalCount'])
        db.session.add(entry)

    def get_average(self):
        self._ElementDict['histAvg'] = int(ScrapeCount.query.with_entities(func.avg(ScrapeCount.count)).first()[0])
        pass



