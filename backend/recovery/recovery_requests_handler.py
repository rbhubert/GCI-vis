from datetime import datetime

import task_handler
from enums import RequestType
from recovery import activity
from recovery import multimedia_interaction
from recovery import news
from recovery.emotions import get_emotions_newspaper, get_emotions_social_media, get_emotions_combinations_social_media, \
    get_emotions_combinations_newspaper
from recovery.wordcloud import get_wordcloud_social_media, get_wordcloud_newspaper


# Checks that socialMedia exists, and then proceeds to get the posts from the user in the timeWindow.
def check_and_get_posts(social_media, user_id, time_window=None):
    social_network = task_handler.__get_social_media_instance(social_media)
    if social_network is None:
        return None  # TODO error message

    if time_window is None:
        return social_network.get_posts(user_id)

    date_window = time_window.split(",")
    since = datetime.strptime(date_window[0], "%Y-%m-%d")
    until = datetime.strptime(date_window[1], "%Y-%m-%d")
    return social_network.get_posts(user_id, since, until)


# Checks that the news (url) exists in DB and then proceeds to get the comments related to that newsItem.
def check_and_get_comments(url):
    comments = news.get_comments(url)
    if comments is None:
        return None  # TODO error message

    return comments


# Calls to get_wordCloud
# - with all the posts from the user in the timeWindow if the requestType is SOCIALMEDIA
# - with all the comments related to the newsUrl if the requestType is NEWSPAPER
# and returns the words for the wordCloud with its emotions and frequency.
def get_wordcloud(request_type, social_media=None, user_id=None, time_window=None, url=None):
    if request_type == RequestType.NEWSPAPER:
        if url is None:
            return {}  # TODO error message

        comments = check_and_get_comments(url)
        return get_wordcloud_newspaper(comments)

    if request_type == RequestType.SOCIALMEDIA:
        if social_media is None or user_id is None:
            return {}  # TODO error message

        posts = check_and_get_posts(social_media, user_id, time_window)
        if posts is None:
            return {}  # TODO error message
        return get_wordcloud_social_media(posts)


# Calls to get_emotionsCombinations
# - with all the posts from the user in the timeWindow if the requestType is SOCIALMEDIA
# - with all the comments related to the newsUrl if the requestType is NEWSPAPER
# and returns the emotions combinations and its values identify in the comments of the posts.
def get_emotions_combinations(request_type, social_media=None, user_id=None, time_window=None, url=None):
    if request_type == RequestType.NEWSPAPER:
        if url is None:
            return {}  # TODO error message
        comments = check_and_get_comments(url)
        return get_emotions_combinations_newspaper(comments)

    if request_type == RequestType.SOCIALMEDIA:
        if social_media is None or user_id is None:
            return {}  # TODO error message

        posts = check_and_get_posts(social_media, user_id, time_window)
        if posts is None:
            return {}  # TODO error message

        return get_emotions_combinations_social_media(posts)


# Calls to get_multimediaInteraction with all the posts from the _userID_ in the _timeWindow_
def get_multimedia_interaction(social_media, user_id, time_window):
    posts = check_and_get_posts(social_media, user_id, time_window)

    if posts is None:
        return {}  # TODO error message

    social_network = task_handler.__get_social_media_instance(social_media)

    return multimedia_interaction.get_multimedia_interaction(social_network.get_multimedia_structure(),
                                                             social_network.get_interaction_structure(),
                                                             posts)


# Calls to get_multimedia with all the posts from the _userID_ in the _timeWindow_
def get_multimedia(social_media, user_id, time_window):
    posts = check_and_get_posts(social_media, user_id, time_window)
    if posts is None:
        return {}  # TODO error message

    social_network = task_handler.__get_social_media_instance(social_media)

    return multimedia_interaction.get_multimedia(social_network.get_multimedia_structure(),
                                                 posts)


# Calls to get_interaction with all the posts from the _userID_ in the _timeWindow_
def get_interaction(social_media, user_id, time_window):
    posts = check_and_get_posts(social_media, user_id, time_window)
    if posts is None:
        return {}  # TODO error message

    social_network = task_handler.__get_social_media_instance(social_media)

    return multimedia_interaction.get_interaction(social_network.get_interaction_structure(),
                                                  posts)


# Calls to get_emotions
# - with all the posts from the user in the timeWindow if the requestType is SOCIALMEDIA
# - with all the comments related to the newsUrl if the requestType is NEWSPAPER
# and returns the dates , number of posts/comments made and the emotions values associated.
def get_emotions(request_type, social_media=None, user_id=None, time_window=None, url=None):
    if request_type == RequestType.NEWSPAPER:
        if url is None:
            return {}  # TODO error message
        comments = check_and_get_comments(url)
        return get_emotions_newspaper(comments)

    if request_type == RequestType.SOCIALMEDIA:
        if social_media is None or user_id is None:
            return {}  # TODO error message
        posts = check_and_get_posts(social_media, user_id, time_window)

        if posts is None:
            return {}  # TODO error message

        return get_emotions_social_media(posts)


# Calls to get_activity with all the posts from the _userID_ in the _timeWindow_
def get_activity(social_media, user_id, time_window):
    posts = check_and_get_posts(social_media, user_id, time_window)
    if posts is None:
        return {}  # TODO error message

    social_network = task_handler.__get_social_media_instance(social_media)

    return activity.get_activity(posts, social_network.get_interaction_structure())
