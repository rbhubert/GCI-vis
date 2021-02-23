from enum import Enum


# This file has the enums required to access the Twitter and Facebook APIs and to the fields of the APIs' responses.

class TwitterAPIAccess:
    AUTH = ("lQO8UHXA1eI6f6sHwAHRxzw6O", "qxdFcpzEvrcawOKPNzoT8pYMJ0AERLayFiENJKPti86PQb9MNi")
    ACCESS_TOKEN = ("3177403715-Q7JqYDyqbUut5kxiLPI6ps7XxHNW7TgcEiJScyy",
                    "3xZMxOKzHKOtOtKQAcluo6uOy97wHxY3nhceQ6Np0K0Rk")
    TWITTER_COOKIES = {"guest_id": "v1:152770215647907451",
                       "gdpr_lo": "1",
                       "_ga": "GA1.2.763768366.1493296891",
                       "personalization_id": "v1_N2Uvt3eLtqi+U7soZuVh6A==",
                       "tfw_exp": "0",
                       "syndication_guest_id": "v1%3A150772492260930324",
                       "__utma": "43838368.763768366.1493296891.1510596801.1510665521.2",
                       "__utmz": "43838368.1510596801.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
                       "dnt": "1",
                       "ads_prefs": "HBESAAA=",
                       "kdt": "GfuSzKBE8yMeyC8RhwX73OfXwR8ULVqB8G3PHnx0",
                       "remember_checked_on": "0",
                       "twid": "u=3177403715",
                       "auth_token": "f16815759ec1d330ea3ba75773ba2b57d26d0c59",
                       "_twitter_sess": "BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%0ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCO4veY1jAToMY3NyZl9p%0AZCIlNDUyNDc1ZWVlYjkxMjdhYmU1MzJkYzM1NWFjMjYxMmQ6B2lkIiU4OTAx%0AYWVmNTI0ZjUzNDhiNTZkZTM1MjMzZTE4MjYwYjoJdXNlcmwrB0NVY70%3D--8ce322ec4d55ce358dcd6c2bfa044e25c039d544",
                       "lang": "es",
                       "ct0": "81a4732a6f7be5f8ba8954770ede14e7",
                       "_gid": "GA1.2.1651483419.1512563244",
                       "external_referer": "padhuUp37zj4cbdtaTy1FTTXL3aYPkK7CyHr8oAJU2c%3D|0|8e8t2xd8A2w%3D",
                       "_gat": "1"
                       }


class TwitterAPIStructure:
    ID = "id_str"
    POST = ("full_text", "text")
    CREATION_TIME = "created_at"
    SOCIAL_NETWORK = "twitter"
    USER = ("user", "id_str", "screen_name")

    HASHTAGS = ("entities", "hashtags", "text")

    RETWEETS = "retweet_count"
    FAVORITES = "favorite_count"

    IMAGE = ("extended_entities", "media", "type", "photo", "expanded_url")
    LINK = ("entities", "urls", "expanded_url")
    VIDEO = ("extended_entities", "media", "type", "video", "expanded_url")

    IN_RESPONSE_TO = "in_reply_to_status_id_str"
    TWEET_MODE = "extended"


class FacebookAPIReactions(Enum):
    LIKE = "like"
    WOW = "wow"
    LOVE = "love"
    HAHA = "haha"
    SAD = "sad"
    ANGRY = "angry"


class FacebookAPIFields:
    ACCESS_TOKEN = "FACEBOOK_ACCESS_TOKEN"
    USER = "?fields=id"
    ALL_INFO = "data"
    FIELDS = "?fields=message,created_time,type,place,picture,source"
    FIELDS_COMMENT = "?fields=message,created_time,attachment"
    SHARED_POSTS = "/sharedposts"
    COMMENTS = "/comments"
    FEED = "/posts"
    ATTACHMENTS = "?fields=link,picture,source"
    PAGINATION = "paging"
    NEXT_PAGE = "next"
    REACTIONS = "?fields=reactions.type(LIKE).summary(total_count).limit(0).as({0}),reactions.type(LOVE).summary(" \
                "total_count).limit(0).as({1}),reactions.type(WOW).summary(total_count).limit(0).as({2})," \
                "reactions.type(HAHA).summary(total_count).limit(0).as({3}),reactions.type(SAD).summary(" \
                "total_count).limit(0).as({4}),reactions.type(ANGRY).summary(total_count).limit(0).as({5})".format(
        FacebookAPIReactions.LIKE.value, FacebookAPIReactions.LOVE.value, FacebookAPIReactions.WOW.value,
        FacebookAPIReactions.HAHA.value, FacebookAPIReactions.SAD.value, FacebookAPIReactions.ANGRY.value)


class FacebookAPIStructure:
    ID = "id"
    POST = "message"
    CREATION_TIME = "created_time"
    TYPE = "type"
    IMAGE = "picture"
    VIDEO = "source"
    SOCIAL_NETWORK = "facebook"
