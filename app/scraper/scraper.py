from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import flash, redirect, url_for
import json
from ..main import errors
import sys


# Main Scraper Class
class Scraper:

    def __init__(self, website):
        if website and self.validate_website(website):
            self._soup = ""
            self._elements = ""
            self._ElementUniqueList = []
            self._ElementList = []
            self._ElementDict = {}

            # Get Website Data
            html = urlopen(website)
            self._soup = BeautifulSoup(html)
            self.elements = self._soup.find_all()


        else:
            flash("the website could not be found")
            redirect(url_for('.index'))

    def validate_website(self, website):
        pass
        return True

    def scrape(self):
        # Get unique list of elements
        for e in self.elements:
            if e.name not in self._ElementUniqueList:
                self._ElementUniqueList.append(e.name)

        # Create list
        self.create_element_list()

        return self._ElementDict

    def create_element_list(self):
        # Creation list of Dictionaries
        for e in self._ElementUniqueList:
            self._ElementList.append({'name':e,
                                      'count':len(self._soup.find_all(e)),
                                      'details':[self.truncate(v) for v in self._soup.find_all(e)]})


        # Sort
        self._ElementList = sorted(self._ElementList, key=lambda k: k['count'], reverse=True)

        self._ElementDict['list'] = self._ElementList

    def truncate(self, v):
        if len(v.text) > 30:
            return v.text[:30] + '..'
        elif v.text == "":
            return "None"
        else:
            return v.text






