import os

import pymongo

from enums.databaseEnums import *
from enums.dbStructure import NewspaperStructure, FollowingStructure
from utils.singleton import Singleton

MONGODB_URI = os.environ.get('MONGODB_URI', DATABASE)


# Database connection. This class is a Singleton.
class Database(metaclass=Singleton):
    def __init__(self):
        client = pymongo.MongoClient(MONGODB_URI)
        db_name = MONGODB_URI.rsplit('/', 1)[-1]
        self.__db = client[db_name]

    def __getitem__(self, item):
        return self.__db[item]


# TODO obtain lexicon depending of language /// spanish or english etc... 
# Class for lexicon/emotions access
class LexiconDB:
    def __init__(self):
        self.db = Database()
        self.collection = DBCollections.LEXICON

    # Retuns the lexicon information associated to the _lexicon_ parameter.
    # If this lexicon is not in the database, it searchs for the _stem_ parameter.
    def get_lexicon(self, lexicon, stem):
        #lexicon_info = self.db[self.collection].find_one({"spanish": lexicon})
        lexicon_info = self.db[self.collection].find_one({"english": lexicon})

        if lexicon_info is None:
            lexicon_info = self.db[self.collection].find_one({"stem": stem})

        return lexicon_info


# Class for user/account store and access.
class AccountsDB:
    def __init__(self):
        self.db = Database()
        self.collection = DBCollections.ACCOUNTS

    # Returns the account asociated to an username and a social network
    def get_account(self, username, socialnetwork):
        account_info = self.db[self.collection].find_one(
            {User.NAME: username, User.SOCIAL_NETWORK: socialnetwork})
        return account_info

    # Returns True is exists an entry in the db with user.id equals to _accountID_
    def exists_accountID(self, accountID):
        return self.db[self.collection].find({User.ID: accountID}).count()

    # Saves the account in the database
    def add_account(self, account):
        return self.db[self.collection].insert(account)

    # Update the username of an account
    def update_account(self, accountID, username):
        self.db[self.collection].update({User.ID: accountID}, {
            DBOperators.SET: {
                User.NAME: username
            }
        })


# Class for posts of Social Media.
class Collection:
    # Collection can be: db/constraint/DBCollections
    def __init__(self, collection):
        self.db = Database()
        self.collection = collection

    # Returns True if the user (_accountID_) has posts in the DB
    def has_posts(self, accountID):
        userId_field = get_userID()
        return self.db[self.collection].find({userId_field: accountID}).count() > 0

    # Returns the posts of the accounts_id
    def get_posts(self, accounts_id):
        userId_field = get_userID()
        posts = self.db[self.collection].find({userId_field: {DBOperators.IN: accounts_id}})
        return posts

    # Returns the posts of all the accounts (ids) in a time window (since-until)
    def get_posts_timewindow(self, accounts_id, since=None, until=None):
        userId_field = get_userID()
        if since is None or until is None:
            posts = self.db[self.collection].find(
                {userId_field: {DBOperators.IN: accounts_id}})
        else:
            posts = self.db[self.collection].find(
                {userId_field: {DBOperators.IN: accounts_id},
                 Structure.CREATION_TIME: {DBOperators.GREATER: since, DBOperators.LESSER: until}})

        return posts

    # Returns the post with "post_id" id
    def get_post(self, post_id):
        return self.db[self.collection].find_one({Structure.ID: post_id})

    # Returns true if post_id is in the collection
    def post_in_db(self, post_id):
        return self.db[self.collection].find({Structure.ID: post_id}).count() > 0

    # Saves post in the collection
    def save_post(self, post_id, original_post, post):
        self.db[get_completeCollection(self.collection)].insert_one(original_post)
        self.db[self.collection].replace_one(filter={Structure.ID: post_id}, replacement=post, upsert=True)

    # Updates the post information (post) that matches the post_id
    def update_post(self, post_id, post):
        self.db[self.collection].replace_one(filter={Structure.ID: post_id}, replacement=post)

    # Returns the posts that will be updated if its 'update' field is True
    def get_posts_to_update(self, accounts):
        userId_field = get_userID()
        posts = self.db[self.collection].find(
            {UPDATE: True, userId_field: {DBOperators.IN: accounts}})
        return posts

    # Returns the latest post published by account_id
    def get_latest_post(self, account_id):
        userId_field = get_userID()
        result = self.db[self.collection].find({userId_field: account_id})
        if result.count():
            return result.sort([(Structure.CREATION_TIME, pymongo.DESCENDING)])[0]
        else:
            return None


# Class for comments in newspapers
class NewspapersDB:
    def __init__(self):
        self.db = Database()
        self.collection = DBCollections.NEWSPAPER

    # Returns the comments to the _new_
    def get_comments_from_new(self, news):
        comments = self.db[self.collection].find_one({NewspaperStructure.URL: news}, {"_id": 0})[
            NewspaperStructure.COMMENTS]
        return comments

    # Saves in the database a newItem (url + list of comments)
    def add_newItem(self, newItem):
        return self.db[self.collection].insert(newItem)

    # Returns the newItem with "new_url" new_url
    def get_newItem(self, new_url):
        return self.db[self.collection].find_one({NewspaperStructure.URL: new_url}, {"_id": 0})

    def update_newItem(self, newItem):
        return self.db[self.collection].replace_one(filter={NewspaperStructure.URL: newItem[NewspaperStructure.URL]},
                                                    replacement=newItem)


class isFollowing:
    def __init__(self):
        self.db = Database()
        self.collection = DBCollections.FOLLOWED

    def is_following(self, userID, account):
        isFollowing = self.db[self.collection].find_one({FollowingStructure.ID: userID},
                                                        {FollowingStructure.Account.SOCIAL_NETWORK: account[0]},
                                                        {FollowingStructure.Account.NAME: account[1]}, {"_id": 0})
        return isFollowing is not None

    # Saves in the database a newItem (url + list of comments)
    def add_following(self, userID, account):
        item = {
            FollowingStructure.ID: userID,
            FollowingStructure.ACCOUNT: {
                FollowingStructure.Account.SOCIAL_NETWORK: account[0],
                FollowingStructure.Account.NAME: account[1]
            }
        }
        return self.db[self.collection].insert(item)


# Creation of a NewspaperDataBase Instance.
newspaperDB = NewspapersDB()
# Creation of a AccountsDataBase Instance.
accountsDB = AccountsDB()
