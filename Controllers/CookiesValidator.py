from curses import raw
import requests
from bs4 import BeautifulSoup
import csv
import os

class CookiesValidator:
    """Receives cookies from user and validates them
        
    Attributes
    ----------
    keyInfo(class) : dict
        Key-value pairs of key info that this CLI program needs to run.
        Examples include the individual cookie values, and header information for the http request module.
    
    headers(class) : dict
        Info that is sent when the this program uses the requests module.
        This info identifies the engineer who is requesting HTTP data.

    domain(class) : string
        The domain that this program is scraping.
        This program concatinates this domain to the found HTTP subdirectories.
        
    cookies(instance) : list
        The cookies that the CLI needs to pass to requests module
    
    testLink(instance) : string
        The test link that the CLI will use, to see if the given cookies work.
    
    
    Methods
    ----------
    areCookiesValidated(none)
        Validates the cookies that the user provides
    """

    
    
    keyInfo = {}

    with open(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Data', 'keyInfo.csv'))) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            keyInfo[row[0]] = row[1]
    
    headers = {
        'User-Agent': keyInfo["User-Agent"],
        'From': keyInfo["From"],
        'Referer': keyInfo["Referer"],
    }
    
    def __init__(self):
        """
        Parameters
        ----------
        none
        """
        
        self._cookies = {
            "mywork.tab.tasks":"false",
            "JSESSIONID":self.keyInfo["JSESSIONID"],
            "_gid":self.keyInfo["_gid"],
            "_ga":self.keyInfo["_ga"],
        }

        self._domain = self.keyInfo["domain"]
        self._testLink = self.keyInfo["urlTestConfluencePage"]

    def __repr__(self):
        return f'CookiesChecker({self._cookies}, {self._testLink})'

    @property
    def cookies(self):
        return self._cookies

    @property
    def domain(self):
        return self._domain

    def areCookiesValidated(self):
        """
        Validates the cookies that the user provides
    
        Parameters
        ----------
        none
    
        Returns
        ----------
        Boolean
            True if the cookies are validated.
            False if the cookies are not validated.
        """
    
        rawPageSource = requests.get(self._testLink, headers=self.headers, cookies=self._cookies)

        soup = BeautifulSoup(rawPageSource.content, "html.parser")

        linkElements = list(soup.find_all("link"))

        linkFound = False

        for element in linkElements:
            if self._testLink in element["href"]:
                linkFound = True

        return linkFound