from http import cookies
from http.cookiejar import Cookie
from selectors import EpollSelector
import sys
from Controllers.MainMenuProvider import MainMenuProvider
from Controllers.ConfluenceLinksGatherer import ConfluenceLinksGatherer
from Controllers.AlternateTextLocator import AlternateTextLocator
from Controllers.RecentAuthorsGatherer import RecentAuthorsGatherer
from Controllers.CSVFileGenerator import CSVFileGenerator
from Controllers.CookiesValidator import CookiesValidator
from Models.DBHandler import DBHandler



mainMenuProvider = MainMenuProvider()

while True:

    while mainMenuProvider.didUserProvideValidOption() is False:

        mainMenuProvider.listMainOptions()
        mainMenuProvider.askUserToChooseOption()

        if mainMenuProvider.didUserProvideValidOption() is False:
            print("Invalid option provided.  Please try again.")

    if mainMenuProvider.optionChosen == "6":
        sys.exit("Program closing now")
    else:
        cookiesValidator = CookiesValidator()

        while cookiesValidator.areCookiesValidated() == False:
            print("Cookies weren't validated.  Please try again.")
            cookiesValidator = CookiesValidator()

        if mainMenuProvider.optionChosen == "1":
            confluenceLinksGatherer = ConfluenceLinksGatherer(
                cookiesValidator.cookies,
                cookiesValidator.headers,
                cookiesValidator.domain
            )
            dbHandler = DBHandler()
            continueLoop = True

            counter = 1

            while continueLoop == True:
                soup = confluenceLinksGatherer.generateSoupSearchPage()
                links = confluenceLinksGatherer.retrieveTenLongLinks(soup)
                dbHandler.addLongLinksToDB(links)
                
                print(f"Finished with search page #{counter}")
                counter+=1

                if confluenceLinksGatherer.isThereANextSearchResultsPage(soup) == False:
                    continueLoop = False
        elif mainMenuProvider.optionChosen == "2":
            dbHandler = DBHandler()

            links = dbHandler.retrieveLongLinks()

            counter = 0
            
            for link in links:
                print(f"Checking page #{counter} now...")
                alternateTextLocator = AlternateTextLocator(
                    link[0],
                    cookiesValidator.cookies,
                    cookiesValidator.headers,
                    cookiesValidator.domain
                )

                if alternateTextLocator.doesPageHaveImages() == False:
                    dbHandler.updateImageNamesLinkColumn(link[0], "No images found")
                else:
                    dbHandler.updateHasImagesColumn(link[0], 1)

                    alternateTextLocator.getImagesMissingAltText()
                    
                    if alternateTextLocator.doAllImagesHaveAltText() == True:
                        dbHandler.updateHasAltTextColumn(link[0], 1)
                        dbHandler.updateImageNamesLinkColumn(link[0], str("Intentionally left blank, since all images have alternate text"))
                    else:
                        dbHandler.updateImageNamesLinkColumn(link[0], str(alternateTextLocator.linksNamesImagesMissingAltText))
                        pageName = alternateTextLocator.retrievePageName()
                        dbHandler.updatePageNameColumn(link[0], pageName)
                counter+=1
            
        elif mainMenuProvider.optionChosen == "3":
            dbHandler = DBHandler()
            dbHandler.removeLinksNoImages()
            dbHandler.removeLinksHaveAltText()
        elif mainMenuProvider.optionChosen == "4":
            recentAuthorsGatherer = RecentAuthorsGatherer()

            # TODO -- Add a method that scrapes all ITS email addresses from UWF directory, adds them to a Python list.  If an author appears on that list, then change the author to me.

        elif mainMenuProvider.optionChosen == "5":
            csvFileGenerator = CSVFileGenerator()

            # TODO -- Write the strings for the bullets for the individualized emails in Python (these strings will be sent to a csv file, along with the author's addresses)

        mainMenuProvider.optionChosen = "previous user option has been reset"