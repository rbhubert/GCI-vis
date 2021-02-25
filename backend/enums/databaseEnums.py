from enums.dbStructure import Structure, User

#DATABASE = "mongodb://localhost:27017/GCI_analysis"
DATABASE = "mongodb://localhost:27017/backend-g-TEST"
UPDATE = "update"


# List of existing collections in the database.
class DBCollections:
    LEXICON = "emotionLexicon"
    ACCOUNTS = "accounts"
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
def get_complete_collection(nameCollection):
    return nameCollection + "_complete"


# Returns the field in the post saved in the database that have the userID.
# In the case of Twitter, the "user.user_id"
def get_user_id():
    return Structure.USER + "." + User.ID
