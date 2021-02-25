# In a database...

# Fields for a User.
class User:
    ID = "user_id"
    NAME = "username"
    SOCIAL_NETWORK = "social_network"


# Fields for a Post (base).
class Structure:
    class Post:
        ORIGINAL = "original"
        SPLITTED = "splitted"

    # Fields for Interactions
    class Interactions:
        COMMENTS = "comments"

        def __len__(self):
            return 1

    # Fields for Multimedia
    class Multimedia:
        IMAGE = "image"
        VIDEO = "video"
        LINK = "link"

        def __iter__(self):
            yield self.IMAGE
            yield self.VIDEO
            yield self.LINK

        def __len__(self):
            return 3

    ID = "id"
    POST = "post"
    CREATION_TIME = "creation_time"
    UPDATE = "update"
    HASHTAGS = "hashtags"
    INTERACTIONS = "interactions"
    MULTIMEDIA = "multimedia"
    SOCIAL_NETWORK = "social_network"
    USER = "user"
    EMOTIONS = "emotions"


# Fields for a Twitter Post. It based on the fields for any kind of Post (Structure)
class TwitterStructure(Structure):
    # Fields for Twitter Interactions.
    class TwitterInteractions(Structure.Interactions):
        RETWEETS = "retweets"
        FAVORITES = "favorites"

        def __iter__(self):
            yield self.COMMENTS
            yield self.RETWEETS
            yield self.FAVORITES

        def __len__(self):
            return super().__len__() + 2


# Fields for a Facebook Post. It based on the fields for any kind of Post (Structure)
class FacebookStructure(Structure):
    # Fields for Twitter Interactions.
    class FacebookInteractions(Structure.Interactions):
        REACTIONS = "reactions"
        SHARES = "shares"

        def __iter__(self):
            yield self.REACTIONS
            yield self.SHARES
            yield self.COMMENTS

        def __len__(self):
            return super().__len__() + 2

    TYPE = "post_type"


class NewspaperStructure:
    class Content:
        SECTION_TITLE = "section_title"
        IMAGE = "images"
        TEXT = "text"
        LINKS = "links"

    class Image:
        URL = "url"
        TEXT = "text"

    class Link:
        URL = "url"
        TEXT = "text"

    class Comments:
        ID = "id"
        USERNAME = "username"
        TEXT = "text"
        CREATION_TIME = "creation_time"
        LIKES = "likes"
        DISLIKES = "dislikes"
        REPLIES = "replies"

    URL = "url"
    TITLE = "title"
    CONTENT_STRUCTURED = "content_structured"
    CONTENT_TEXT = "content_text"
    CREATION_TIME = "creation_time"
    COMMENTS = "comments"
    LAST_COMMENT = "last_comment"


class FollowingStructure:
    USERNAME = "username"
    SOCIAL_NETWORK = "social_network"
    ID = "user_id"
