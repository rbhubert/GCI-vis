from enums.dbStructure import Structure, User

DATABASE = "mongodb://localhost:27017/backend-g-TEST"
# DATABASE = "mongodb://localhost:27017/backend-g_localhost"
UPDATE = "update"


# List of existing collections in the database.
class DBCollections:
    LEXICON = "emotionLexicon"
    ACCOUNTS = "accounts"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    NEWSPAPER = "newspaper"
    FOLLOWED = "followed"


# Operators of mongo.
class DBOperators:
    IN = "$in"
    GREATER = "$gte"
    LESSER = "$lte"
    SET = "$set"


# Returns the collection where the unstructured posts have to be saved
# In the case of Twitter, the "twitter" collection will have the structured posts, and "twitter_complete"
# the unstructured ones.
def get_completeCollection(nameCollection):
    return nameCollection + "_complete"


# Returns the field in the post saved in the database that have the userID.
# In the case of Twitter, the "user.user_id"
def get_userID():
    return Structure.USER + "." + User.ID
