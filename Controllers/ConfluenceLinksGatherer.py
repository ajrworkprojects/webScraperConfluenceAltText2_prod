from http import cookies
from http.cookiejar import Cookie
import requests, time
from bs4 import BeautifulSoup
import csv
import os

class ConfluenceLinksGatherer:
    """Gathers links to all PKB pages.
        
    Attributes
    ----------
    keyInfo(class) : dict
        Key-value pairs of key info that this CLI program needs to run.
        ConfluenceLinksGatherer only uses one of these key-value pairs, the url for the initial Confluence search page.
    
    urlInitialSearchPage(class) : string
        URL to the initial search page in Confluence

    urlNextSearchPage(class) : string
        URL to whatever the next search page in Confluence is  

    cookies(instance): dict
        Key-value pairs of the necessary cookies for logging in to Confluence

    headers(instance): dict
        Key-value pairs of the necessary data to pass to requests module

    domain(instance): string
        The domain of the main Confluence site to search  
    
    Methods
    ----------
    instanceMethodName(parameter)
        Brief desc of method
    """

    keyInfo = {}

    with open(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Data', 'keyInfo.csv'))) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            keyInfo[row[0]] = row[1]
    
    urlInitialSearchPage = keyInfo["urlInitialSearchPage"]

    urlNextSearchPage = "not found yet"
    
    def __init__(self, cookies, headers, domain):
        """
        Parameters
        ----------
        cookies: dict
            Key-value pairs of the necessary cookies for logging in to Confluence

        headers: dict
            Key-value pairs of the necessary data to pass to requests module

        domain: str
            The domain of the main Confluence site to search
        """

        self._cookies = cookies
        self._headers = headers
        self._domain = domain

    def __repr__(self):
        return f'ConfluenceLinksGatherer()'

    @property
    def cookies(self):
        return self._cookies

    @property
    def headers(self):
        return self._headers

    @property
    def domain(self):
        return self._domain

    def generateSoupSearchPage(self):
        """
        Generate readable html of a Confluence search page
    
        Parameters
        ----------
        none
    
        Returns
        ----------
        BeautifulSoup
            Neat html of search results page
        """
    
        time.sleep(20)
        
        url = ""

        if ConfluenceLinksGatherer.urlNextSearchPage == "not found yet":
            url = ConfluenceLinksGatherer.urlInitialSearchPage
        else:
            url = ConfluenceLinksGatherer.urlNextSearchPage
        
        rawPageSource = requests.get(url, cookies=self._cookies, headers=self._headers)

        return BeautifulSoup(rawPageSource.content, "html.parser")

    def isThereANextSearchResultsPage(self, soup):
        """
        Checks to see if there's another page of search results.
        Also updates urlNextSearchPage variable with either the url to the next search page, or with "no next link".
    
        Parameters
        ----------
        soup : BeautifulSoup
            More readable html of the current search results page.
    
        Returns
        ----------
        boolean
            True if there's another page of search results, false if not.
        """
        
        elementNextSearchPage = list(soup.find_all("a", class_="pagination-next"))

        if elementNextSearchPage:
            ConfluenceLinksGatherer.urlNextSearchPage = self._domain + elementNextSearchPage[0]["href"]
            return True
        else:
            ConfluenceLinksGatherer.urlNextSearchPage = "no next link"
            return False

    def retrieveTenLongLinks(self, soup):
        """
        Retrieves the long links to the specific Confluence pages that appear on a given search page.
        Will be no more than ten links to retrieve.
    
        Parameters
        ----------
        soup : BeautifulSoup
            More readable html of the current search results page.
    
        Returns
        ----------
        list
            long links to specific Confluence pages.
        """
    
        elementsLongLinks = list(soup.find_all("a", class_="search-result-link visitable"))

        urlsLongLinks = []

        for element in elementsLongLinks:
            urlsLongLinks.append(self._domain + element["href"])

        return urlsLongLinks