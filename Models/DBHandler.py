import sqlite3
from datetime import datetime

class DBHandler:
    """Makes updates to webscraper.db
        
    Attributes
    ----------
    None
    
    Methods
    ----------
    addLongLinksToDB(links)
        Adds long links to db, if those links aren't already in db.
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """

    def __repr__(self):
        return f'DBHandler()'

    def addLongLinksToDB(self, links):
        """
        Adds long links to db, if those links aren't already in db.
        This method adds links in groups of ten (because there are no more than ten links on a Confluence search page).
    
        Parameters
        ----------
        links : list
            Long links to add to db.
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        for link in links:
            if dbCursor.execute("SELECT * FROM CONFLUENCE_PAGES WHERE longLink = (?)", (link,)).fetchone() == None:
                dbCursor.execute("INSERT INTO CONFLUENCE_PAGES (longLink) VALUES (?)", (link,))

        dbConnector.commit()
        dbConnector.close()

    def retrieveLongLinks(self):
        """
        Retrieves all long links currently in db.
    
        Parameters
        ----------
        none
    
        Returns
        ----------
        list
            All links currently in db.
            The list contains one-item tuples.
        """
    
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("SELECT longLink FROM CONFLUENCE_PAGES")

        links = dbCursor.fetchall()

        dbConnector.commit()
        dbConnector.close()

        return links

    def updateHasImagesColumn(self, longLink, value):
        """
        Receives a long link and updates the hasImages column with the given value
    
        Parameters
        ----------
        longLink : tuple
            A one-item tuple containing the long link in the db that's about to get updated.

        value : int
            The value to add to the db (either a 0 or 1; 0 = false; 1 = true)
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("""UPDATE CONFLUENCE_PAGES 
                            SET hasImages = (?)
                            WHERE longLink = (?)""", (value, longLink))

        dbConnector.commit()
        dbConnector.close()

    def updateHasAltTextColumn(self, longLink, value):
        """
        Receives a long link and updates the hasAltText column with the given value
    
        Parameters
        ----------
        longLink : tuple
            A one-item tuple containing the long link in the db that's about to get updated.

        value : int
            The value to add to the db (either a 0 or 1; 0 = false; 1 = true)
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("""UPDATE CONFLUENCE_PAGES 
                            SET hasAltText = (?)
                            WHERE longLink = (?)""", (value, longLink))

        dbConnector.commit()
        dbConnector.close()

    def updateImageNamesLinkColumn(self, longLink, value):
        """
        Receives a long link and updates the imageNamesLinks column with the given value
    
        Parameters
        ----------
        longLink : tuple
            A one-item tuple containing the long link in the db that's about to get updated.

        value : string
            The value to add to the db.

            NOTE -- This value is a single dictionary variable that may contain a number of key-value pairs.  SQLite will convert this variable to a string of a list of key-value pairs, and each pair is in its own tuple.
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("""UPDATE CONFLUENCE_PAGES 
                            SET imageNamesLinks = (?)
                            WHERE longLink = (?)""", (value, longLink))

        dbConnector.commit()
        dbConnector.close()

    def updatePageNameColumn(self, longLink, value):
        """
        Receives a long link and updates the pageName column with the given value
    
        Parameters
        ----------
        longLink : tuple
            A one-item tuple containing the long link in the db that's about to get updated.

        value : string
            The value to add to the db 
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("""UPDATE CONFLUENCE_PAGES 
                            SET pageName = (?)
                            WHERE longLink = (?)""", (value, longLink))

        dbConnector.commit()
        dbConnector.close()

    def updateDateAddedToDBColumn(self, longLink):
        """
        Updates the dateAddedToDB column with today's date, in YYYY-MM-DD format.
    
        Parameters
        ----------
        link : str
            The long link to the Confluence page.
    
        Returns
        ----------
        None
        """
    
        todaysDate = datetime.today().strftime('%Y-%m-%d')
        
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("""UPDATE CONFLUENCE_PAGES 
                            SET dateAddedToDB = (?)
                            WHERE longLink = (?)""", (todaysDate, longLink))

        dbConnector.commit()
        dbConnector.close()

    def removeLinksNoImages(self):
        """
        Remove links from DB, if the pages currently have no images.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("""DELETE FROM CONFLUENCE_PAGES 
                            WHERE hasImages = 0""")

        dbConnector.commit()
        dbConnector.close()

    def removeLinksHaveAltText(self):
        """
        Remove links from DB, if a page has images, and if all of those images have alternate text.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect("Data/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("""DELETE FROM CONFLUENCE_PAGES 
                            WHERE hasImages = 1
                            AND hasAltText = 1""")

        dbConnector.commit()
        dbConnector.close()