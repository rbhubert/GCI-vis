from apis.facebook import Facebook
from apis.twitter import Twitter
from apis.twitter import TwitterStreaming
from database.database import accountsDB
from enums.databaseEnums import DBCollections
from enums.dbStructure import User


def get_socialMediaInstance(socialMedia):
    # we have to create the corresponding socialmedia
    if socialMedia == DBCollections.TWITTER:
        smInstance = Twitter()
    elif socialMedia == DBCollections.FACEBOOK:
        smInstance = Facebook()
    else:
        return False  # there was a error todo error message
    return smInstance


def get_streamingInstance(socialMedia):
    # we have to create the corresponding socialmedia
    if socialMedia == DBCollections.TWITTER:
        smInstance = TwitterStreaming()
    # elif socialMedia == DBCollections.FACEBOOK:
    #     smInstance = Facebook()
    else:
        return False  # there was a error todo error message
    return smInstance


def get_userID(socialMedia, username):
    smInstance = get_socialMediaInstance(socialMedia)
    account_information = accountsDB.get_account(username, socialMedia)
    if account_information is None:
        account_information = smInstance.get_accountInformation(username)
        exists_in_DB = accountsDB.exists_accountID(account_information[User.ID])
        if exists_in_DB:
            accountsDB.update_account(account_information[User.ID], username)
        else:
            accountsDB.add_account(account_information)

    # we notify the socialMedia about the account
    userID = account_information[User.ID]
    return userID


def stream_account(socialMedia, username):
    account_information = accountsDB.get_account(username, socialMedia)
    smInstance = get_streamingInstance(socialMedia)
    smInstance.add_toStream(account_information[User.ID])
    return True


def remove_account(socialMedia, username):
    account_information = accountsDB.get_account(username, socialMedia)
    smInstance = get_streamingInstance(socialMedia)
    smInstance.remove_ofStream(account_information[User.ID])
    return True

def add_account(socialMedia, username):
    print('Starting task')

    smInstance = get_socialMediaInstance(socialMedia)
    userID = get_userID(socialMedia, username)
    result = smInstance.add_account(userID)

    print('Task completed')
    return result
