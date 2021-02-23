from database.database import newspaperDB
from enums.dbStructure import NewspaperStructure
from newspapers.getNewItem_comments import get_newItem, get_latestComments
from utils.singleton import Singleton


class NewsManager(metaclass=Singleton):
    __instance = None

    def get_newItem(self, new_url):
        newItemR = newspaperDB.get_newItem(new_url)
        if newItemR is not None:  # newItem exists in db
            newComments = get_latestComments(newItemR)
            last_idC = newItemR[NewspaperStructure.LAST_COMMENT]
            if newComments[1] == last_idC:
                return newItemR
            newItemR[NewspaperStructure.COMMENTS].extend(newComments[0])
            newItemR[NewspaperStructure.LAST_COMMENT] = newComments[1]
            newspaperDB.update_newItem(newItemR)
            return newItemR

        newItem = get_newItem(new_url)
        newspaperDB.add_newItem(newItem)
        return newItem

    def searchNewComments(self, new_url):
        newItem = newspaperDB.get_newItem(new_url)
        if newItem is not None:  # newItem exists in db
            return False  # TODO error message
        else:
            newComments = get_latestComments(newItem)
            last_idC = newItem[NewspaperStructure.LAST_COMMENT]
            if newComments[1] == last_idC:
                return newItem

            newItem[NewspaperStructure.COMMENTS].extend(newComments[0])
            newItem[NewspaperStructure.LAST_COMMENT] = newComments[1]
            newspaperDB.update_newItem(newItem)

    def getComments(self, new_url):
        newItem = newspaperDB.get_newItem(new_url)
        if newItem is not None:  # newItem exists in db
            return newItem[NewspaperStructure.COMMENTS]

        return None  # TODO error message


# Creation of an NewspaperManager instance.
newsManager = NewsManager()
