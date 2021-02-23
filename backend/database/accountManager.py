from enum import Enum

from apis.facebook import Facebook
from apis.twitter import Twitter
from database.database import accountsDB
from enums.databaseEnums import DBCollections
from enums.dbStructure import User


class SocialMediaDict(Enum):
    INSTANCE = "social_network"
    ACCOUNTS = "accounts"


# Class/dbConnection to keep track of the accounts that are currently being followed.
# Keep track of the accounts and social networks to which they are linked.
class AccountManager:
    __socialMedias = {}
    __accounts = {}

    # This method adds the account to the list of accounts being currently followed.
    # First, it checks that the socialmedia instance exists, and then calls the add_account of the corresponding
    # socialmedia.
    def add_account(self, socialmedia, username):
        print("AccountManager| Following account")

        # account already in list of account currently followed
        if username in self.__accounts:
            return True  # no errors

        # check socialMedia exists...
        if socialmedia in self.__socialMedias.keys():
            # socialMedia singleton exits.
            sm = self.__socialMedias[socialmedia][SocialMediaDict.INSTANCE]
        else:
            # we have to create the corresponding socialmedia
            if socialmedia == DBCollections.TWITTER:
                sm = Twitter()
            elif socialmedia == DBCollections.FACEBOOK:
                sm = Facebook()
            else:
                return False  # there was a error

            self.__socialMedias[socialmedia] = {
                SocialMediaDict.INSTANCE: sm,
                SocialMediaDict.ACCOUNTS: {}
            }

        account_information = accountsDB.get_account(username, socialmedia)
        if account_information is None:
            account_information = sm.get_accountInformation(username)
            exists_in_DB = accountsDB.exists_accountID(account_information[User.ID])
            if exists_in_DB:
                accountsDB.update_account(account_information[User.ID], username)
            else:
                accountsDB.add_account(account_information)

        # we notify the socialMedia about the account
        userID = account_information[User.ID]
        result = sm.add_account(userID)
        print(account_information)
        # if there was no problem, we add the account in both dicts
        if result:
            if userID not in self.__socialMedias[socialmedia][SocialMediaDict.ACCOUNTS]:
                self.__socialMedias[socialmedia][SocialMediaDict.ACCOUNTS][userID] = username
                self.__accounts[username] = {User.ID: userID,
                                             User.SOCIAL_NETWORK: socialmedia}
        print(self.__accounts)
        return result

    # This methods removes the account of the list of accounts being currently followed.
    # It also calls the remove_account of the corresponding socialmedia.
    def remove_account(self, socialmedia, username):
        print("AccountManager| Removing account")

        if username not in self.__accounts:
            return False  # there was an error
        else:
            userID = self.__accounts[username][User.ID]
            if socialmedia in self.__socialMedias.keys():
                # we notify the socialmedia about the removal
                self.__socialMedias[socialmedia][SocialMediaDict.INSTANCE].remove_account(username)
                self.__socialMedias[socialmedia][SocialMediaDict.ACCOUNTS].pop(userID)

            self.__accounts.pop(username)  # remove from the accounts dict

            return True

    # Returns the ID related to the _username_
    def get_userID(self, username):
        print("------")
        print(self._instance)
        print(username)
        print(self.__accounts)
        print("------")

        if username in self.__accounts:
            return self.__accounts[username][User.ID]

    # This method returns all the followed accounts like tuples (*socialMedia, [*username])
    def get_accounts(self):
        print("AccountManager| Getting all accounts followed")

        tuplesReturn = []
        for k, v in self.__socialMedias.items():
            for account in v[SocialMediaDict.ACCOUNTS].values():
                tuplesReturn.append([k, account])
        return {
            "accounts": tuplesReturn
        }

    # This method returns the social media instance corresponding to socialMedia.
    def get_socialMedia(self, socialMedia):
        if socialMedia in self.__socialMedias.keys():
            return self.__socialMedias[socialMedia][SocialMediaDict.INSTANCE]
        else:
            return None
