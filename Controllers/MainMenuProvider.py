class MainMenuProvider:
    """Provides menu of options to the user
        
    Attributes
    ----------
    optionChosen(instance) : string
        The option that the user chooses.
    
    
    Methods
    ----------
    instanceMethodName(parameter)
        Brief desc of method
    """
    
    def __init__(self):
        """
        Parameters
        ----------
        none
        """

        self._optionChosen = "user hasn't provided option"            

    def __repr__(self):
        return f'MainMenuProvider()'
    
    @property
    def optionChosen(self):
        return self._optionChosen

    @optionChosen.setter
    def optionChosen(self, value):
        self._optionChosen = value
    
    def listMainOptions(self):
        """
        List the main options for the user
    
        Parameters
        ----------
        none
    
        Returns
        ----------
        none
        """
    
        print("\nMain menu options")
        print("-----------------")
        print("1. Get links to all PKB Confluence pages and add them to CLI database.")
        print("2. Check all PKB Confluence links currently in database, for images missing alternate text.")
        print("3. Remove all links to PKB Confluence pages that have no images, or are not missing alternate text.")
        print("4. Get recent authors for all PKB Confluence pages that have images with missing alternate text.")
        print("5. Generate .csv file of authors to contact.")
        print("6. Close program.")
        print("-----------------")

    def askUserToChooseOption(self):
        """
        Ask user to choose option from main menu list.
    
        Parameters
        ----------
        none
    
        Returns
        ----------
        None
        """

        self._optionChosen = input("Please choose a valid option from the list above: ")

    def didUserProvideValidOption(self):
        """
        Brief desc of method
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        boolean
            True if user provided a valid optoin, false otherwise.
        """
    
        if self._optionChosen in "1 2 3 4 5 6" and len(self._optionChosen) == 1:
            return True
        else:
            return False