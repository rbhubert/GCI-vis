import abc


# Class base for any kind of SocialMedia.
class SocialMedia:
    def __init__(self):
        self.NAME = ""
        # self.ACCOUNT_COLLECTION = AccountsDB()
        self.dbCollection = None

    @abc.abstractmethod
    def add_account(self, accountID):
        print(self.NAME + "| Adding account...")
        pass

    @abc.abstractmethod
    def remove_account(self, accountID):
        print(self.NAME + "| Removing account...")
        pass

    # This method returns the posts from an account between the dates determined by the since and until parameters.
    def get_posts(self, accountID, since=None, until=None):
        print(self.NAME + "| Recovering posts from the DB...")
        if since is None or until is None:
            posts = self.dbCollection.get_posts([accountID])
        else:
            posts = self.dbCollection.get_posts_timewindow([accountID], since, until)
        return posts

    # This method updates the interactions values of the accounts.
    # It first gets all the posts of these accounts that will be updated.
    def update_posts(self, accounts):
        print(self.NAME + "| Updating posts interactions...")
        posts_to_update = self.dbCollection.get_posts_to_update(accounts)
        self.__update_posts(posts_to_update)

    @abc.abstractmethod
    def __update_posts(self, posts):
        pass

    # Returns the multimediaStructure related to the socialMedia instance.
    @abc.abstractmethod
    def getMultimediaStructure(self):
        pass

    # Returns the interactionStructure related to the socialMedia instance.
    @abc.abstractmethod
    def getInteractionStructure(self):
        pass
