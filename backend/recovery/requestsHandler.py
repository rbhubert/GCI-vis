from datetime import datetime

import tasks_requestHandler
from enums import RequestType
from newsManager import newsManager
from recovery.activity import get_activity
from recovery.emotions import get_emotions_newspaper, get_emotions_socialMedia, get_emotionsCombinations_socialMedia, \
    get_emotionsCombinations_newspaper
from recovery.multimediaInteraction import get_multimediaInteraction, get_multimedia, get_interaction
from recovery.wordCloud import get_wordCloud_socialMedia, get_wordCloud_newspaper


# Checks that socialMedia exists, and then proceeds to get the posts from the user in the timeWindow.
def check_and_getPosts(socialMedia, userID, timeWindow=None):
    socialNetwork = tasks_requestHandler.get_socialMediaInstance(socialMedia)
    if socialNetwork is None:
        return None  # TODO error message

    if timeWindow is None:
        return socialNetwork.get_posts(userID)

    dateWindow = timeWindow.split(",")
    since = datetime.strptime(dateWindow[0], "%Y-%m-%d")
    until = datetime.strptime(dateWindow[1], "%Y-%m-%d")
    return socialNetwork.get_posts(userID, since, until)


# Checks that the news (url) exists in DB and then proceeds to get the comments related to that newsItem.
def check_and_getComments(url):
    comments = newsManager.getComments(url)
    if comments is None:
        return None  # TODO error message

    return comments


# Calls to get_wordCloud
# - with all the posts from the user in the timeWindow if the requestType is SOCIALMEDIA
# - with all the comments related to the newsUrl if the requestType is NEWSPAPER
# and returns the words for the wordCloud with its emotions and frequency.
def wordCloud(requestType, socialMedia=None, userID=None, timeWindow=None, url=None):
    if requestType == RequestType.NEWSPAPER:
        if url is None:
            return {}  # TODO error message

        comments = check_and_getComments(url)
        return get_wordCloud_newspaper(comments)

    if requestType == RequestType.SOCIALMEDIA:
        if socialMedia is None or userID is None:
            return {}  # TODO error message

        posts = check_and_getPosts(socialMedia, userID, timeWindow)
        if posts is None:
            return {}  # TODO error message
        return get_wordCloud_socialMedia(posts)


# Calls to get_emotionsCombinations
# - with all the posts from the user in the timeWindow if the requestType is SOCIALMEDIA
# - with all the comments related to the newsUrl if the requestType is NEWSPAPER
# and returns the emotions combinations and its values identify in the comments of the posts.
def emotionsCombinations(requestType, socialMedia=None, userID=None, timeWindow=None, url=None):
    if requestType == RequestType.NEWSPAPER:
        if url is None:
            return {}  # TODO error message
        comments = check_and_getComments(url)
        return get_emotionsCombinations_newspaper(comments)

    if requestType == RequestType.SOCIALMEDIA:
        if socialMedia is None or userID is None:
            return {}  # TODO error message

        posts = check_and_getPosts(socialMedia, userID, timeWindow)
        if posts is None:
            return {}  # TODO error message

        return get_emotionsCombinations_socialMedia(posts)


# Calls to get_multimediaInteraction with all the posts from the _userID_ in the _timeWindow_
def multimediaInteraction(socialMedia, userID, timeWindow):
    posts = check_and_getPosts(socialMedia, userID, timeWindow)

    if posts is None:
        return {}  # TODO error message

    socialNetwork = tasks_requestHandler.get_socialMediaInstance(socialMedia)

    return get_multimediaInteraction(socialNetwork.getMultimediaStructure(), socialNetwork.getInteractionStructure(),
                                     posts)


# Calls to get_multimedia with all the posts from the _userID_ in the _timeWindow_
def getMultimedia(socialMedia, userID, timeWindow):
    posts = check_and_getPosts(socialMedia, userID, timeWindow)
    if posts is None:
        return {}  # TODO error message

    socialNetwork = tasks_requestHandler.get_socialMediaInstance(socialMedia)

    return get_multimedia(socialNetwork.getMultimediaStructure(),
                          posts)


# Calls to get_interaction with all the posts from the _userID_ in the _timeWindow_
def getInteraction(socialMedia, userID, timeWindow):
    posts = check_and_getPosts(socialMedia, userID, timeWindow)
    if posts is None:
        return {}  # TODO error message

    socialNetwork = tasks_requestHandler.get_socialMediaInstance(socialMedia)

    return get_interaction(socialNetwork.getInteractionStructure(),
                           posts)


# Calls to get_emotions
# - with all the posts from the user in the timeWindow if the requestType is SOCIALMEDIA
# - with all the comments related to the newsUrl if the requestType is NEWSPAPER
# and returns the dates , number of posts/comments made and the emotions values associated.
def getEmotions(requestType, socialMedia=None, userID=None, timeWindow=None, url=None):
    if requestType == RequestType.NEWSPAPER:
        if url is None:
            return {}  # TODO error message
        comments = check_and_getComments(url)
        return get_emotions_newspaper(comments)

    if requestType == RequestType.SOCIALMEDIA:
        if socialMedia is None or userID is None:
            return {}  # TODO error message
        posts = check_and_getPosts(socialMedia, userID, timeWindow)

        if posts is None:
            return {}  # TODO error message

        return get_emotions_socialMedia(posts)


# Calls to get_activity with all the posts from the _userID_ in the _timeWindow_
def getActivity(socialMedia, userID, timeWindow):
    posts = check_and_getPosts(socialMedia, userID, timeWindow)
    if posts is None:
        return {}  # TODO error message

    socialNetwork = tasks_requestHandler.get_socialMediaInstance(socialMedia)

    return get_activity(posts, socialNetwork.getInteractionStructure())
