from bs4 import BeautifulSoup
import requests, time

class AlternateTextLocator:
    """Checks all Confluence pages already in db, to see if they have images, and if those images have alternate text.
        
    Attributes
    ----------
    link(instance) : string
        The long link to a specific Confluence page.

    cookies(instance): dict
        Key-value pairs of the necessary cookies for logging in to Confluence

    headers(instance): dict
        Key-value pairs of the necessary data to pass to requests module

    domain(instance): str
        The domain of the main Confluence site to search

    rawPageSource(instance) : class 'requests.models.Response
        The value returned when sending the Confluence link to the requests Python module

    soup(instance) : BeautifulSoup
        The neat html code of the rawPageSource

    allElementsImages(instance) : list
        All embedded image elements on a given Confluence page

    linksNamesImagesMissingAltText(instance) : list
        A list of key-value pairs of the images missing alternate text.
        The key will be the url to the image, and the value will be the name of the image    
    
    Methods
    ----------
    instanceMethodName(parameter)
        Brief desc of method
    """
    
    def __init__(self, link, cookies, headers, domain):
        """
        Parameters
        ----------
        link : string
            The long link to a specific Confluence page.
        """

        self._link = link
        self._cookies = cookies
        self._headers = headers
        self._domain = domain

        time.sleep(20)
        self._rawPageSource = requests.get(link, cookies=self._cookies, headers=self._headers)
        self._soup = BeautifulSoup(self._rawPageSource.content, "html.parser")

        self._allElementsImages = []
        self._linksNamesImagesMissingAltText = []

    def __repr__(self):
        return f'AlternateTextLocator({self._link}, self._rawpageSource, self._soup)(some values repressed because of length)'

    @property
    def linksNamesImagesMissingAltText(self):
        return self._linksNamesImagesMissingAltText
    
    def doesPageHaveImages(self):
        """
        Checks to see if a page has images.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        boolean
            True if a page has images.  False if there are no images.
        """
    
        self._allElementsImages = list(self._soup.find_all("img", class_="confluence-embedded-image"))

        if len(self._allElementsImages) == 0:
            return False
        else:
            return True
    
    def getImagesMissingAltText(self):
        """
        Gets the names of, and the links to all the images missing alternate text, then adds the values to the linksNamesImagesMissingAltText variable.
        
        If all images have alternate text, then this variable will be an empty string.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        None
        """

        elementsMissingAltText = []

        for element in self._allElementsImages:
            try:
                if element["alt"]:
                    pass
            except:
                elementsMissingAltText.append(element)

        for element in elementsMissingAltText:

            imageName = ""
            imageLink = self._domain + element["src"]
            
            try:
                imageName = element["data-linked-resource-default-alias"]
            except:
                imageName = "image is embedded from an external website"

            if imageName == "image is embedded from an external website":
                imageLink = element["src"]
            else:
                imageLink = self._domain + element["src"]

            self._linksNamesImagesMissingAltText.append({imageLink: imageName})

    def doAllImagesHaveAltText(self):
        """
        Checks to see if a page has images with missing alternate text.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        boolean
            True if all images have alternate text, and false if images are missing alternate text.
        """
    
        if len(self._linksNamesImagesMissingAltText) == 0:
            return True
        else:
            return False

    def retrievePageName(self):
        """
        Retrieves the name of a given Confluence page
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        String
            name of Confluence page
        """
    
        elementPageName = self._soup.find_all("meta", attrs={"name": "ajs-page-title"})

        return elementPageName[0]["content"]