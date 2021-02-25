from apis.twitter import Twitter
from database.database import accountsDB, followedDB
from enums.databaseEnums import DBCollections
from enums.dbStructure import FollowingStructure
from enums.dbStructure import User


def __get_social_media_instance(social_media):
    # we have to create the corresponding socialmedia
    if social_media == DBCollections.TWITTER:
        sm_instance = Twitter()
    else:
        return False  # there was a error todo error message
    return sm_instance


def __check_user(social_media, username):
    account_information = accountsDB.get_account(username, social_media)

    if account_information is None:
        sm_instance = __get_social_media_instance(social_media)
        account_information = sm_instance.get_account_information(username)
        exists_in_DB = accountsDB.exists_accountID(account_information[User.ID])
        if exists_in_DB:
            accountsDB.update_account(account_information[User.ID], username)
        else:
            accountsDB.add_account(account_information)

    return account_information[User.ID]


def follow_account(social_media, username):
    sm_instance = __get_social_media_instance(social_media)
    user_id = __check_user(social_media, username)

    sm_instance.add_account(user_id)  # first it recovers latests tweets

    followedDB.add_following(user_id, [username, social_media])
    return True


def unfollow_account(social_media, username):
    user_id = __check_user(social_media, username)

    sm_instance = __get_social_media_instance(social_media)
    sm_instance.remove_account(user_id)
    followedDB.remove_following(user_id=user_id, social_media=social_media)
    return True


def get_accounts():
    accounts = followedDB.get_followed()
    tuples = []

    for account in accounts:
        tuples.append([account[FollowingStructure.SOCIAL_NETWORK], account[FollowingStructure.USERNAME]])

    return {
        "accounts": tuples
    }
