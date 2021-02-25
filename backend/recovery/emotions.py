import datetime

import pandas

from enums import Responses
from enums.Emotions import Emotions, EmotionsMiddle
from enums.dbStructure import Structure
from utils import get_emotions
from utils.utils_date import daterange, daterange_hours


# Returns the emotions and combinations between them associated with the _posts_
def get_emotions_combinations_social_media(posts):
    # dict get_emotions_social_media
    # {
    #   emotion : value,
    #   etc
    #   }
    posts = list(posts)
    all_emotions = [pandas.Series(get_emotions.get_emotions_social_media(post)) for post in posts]
    all_emotions_df = pandas.DataFrame(all_emotions)

    sum_emotions = all_emotions_df.sum(axis=0)
    return __create_RadarDataframe(sum_emotions)


# Returns the emotions and combinations between them associated with the _comments_ to a newspaper
def get_emotions_combinations_newspaper(comments):
    posts = list(comments)
    all_emotions = [pandas.Series(get_emotions.get_emotions_news_comment(post)) for post in posts]
    all_emotions_df = pandas.DataFrame(all_emotions)

    sum_emotions = all_emotions_df.sum(axis=0)
    return __create_RadarDataframe(sum_emotions)


# Creates Dataframe from the list _posts_ and calculates the size of each emotions related
# to the posts.
def __create_RadarDataframe(sum_emotions):
    emotions_to_return = {
        Responses.EMOTIONS: {},
        Responses.KEYS: []
    }

    i_aux = ""
    for emotion in Emotions:
        emotions_to_return[Responses.KEYS].append(emotion.value)
        emotions_to_return[Responses.EMOTIONS][emotion.value] = int(sum_emotions[emotion.value])
        emotions_to_return[Responses.EMOTIONS][i_aux] = 0
        i_aux += " "

    i_aux = ""
    for emotion in EmotionsMiddle:
        emotions = emotion.value.split("-")
        emotions_to_return[Responses.EMOTIONS][i_aux] = (emotions_to_return[Responses.EMOTIONS][emotions[0]] +
                                                         emotions_to_return[Responses.EMOTIONS][emotions[1]]) / 2
        i_aux += " "

    return emotions_to_return


# Returns the emotions associated with the _posts_
def get_emotions_social_media(posts):
    posts = list(posts)

    series = []
    for post in posts:
        emotions = get_emotions.get_emotions_social_media(post)
        emotions[Structure.CREATION_TIME] = post[Structure.CREATION_TIME]
        series.append(pandas.Series(emotions))

    all_emotions_df = pandas.DataFrame(series)
    return __create_BubbleDataframe(all_emotions_df)


# Returns the emotions associated with the _comments_ to a news.
def get_emotions_newspaper(comments):
    posts = list(comments)

    series = []
    for post in posts:
        emotions = get_emotions.get_emotions_news_item(post)
        emotions[Structure.CREATION_TIME] = post[Structure.CREATION_TIME]
        series.append(pandas.Series(emotions))

    all_emotions_df = pandas.DataFrame(series)
    return __create_BubbleDataframe_newspaper(all_emotions_df)


# Creates a Dataframe from the list _posts_ and identifies the dates and the number of comments and
# the emotions associated with that date.
def __create_BubbleDataframe(all_data_df):
    min_date = all_data_df[Structure.CREATION_TIME].min()
    max_date = all_data_df[Structure.CREATION_TIME].max()

    emotions_to_return = {}
    for dt in daterange(min_date, max_date):
        ndate = dt.strftime("%Y-%m-%d")
        posts_in_ndate = all_data_df.loc[pandas.to_datetime(all_data_df[Structure.CREATION_TIME].dt.date) == ndate]
        emotions_to_return[ndate] = {
            Responses.VALUE: len(posts_in_ndate),
            Responses.EMOTIONS: {}
        }
        for emotion in Emotions:
            emotions_to_return[ndate][Responses.EMOTIONS][emotion.value] = sum(posts_in_ndate[emotion.value])

    return emotions_to_return


# Creates a Dataframe from the list _posts_ and identifies the dates and the number of comments and
# the emotions associated with that date.
def __create_BubbleDataframe_newspaper(all_data_df):
    min_date = all_data_df[Structure.CREATION_TIME].min()
    max_date = all_data_df[Structure.CREATION_TIME].max()

    emotions_to_return = {}
    for dt_timestamp in daterange_hours(min_date, max_date):
        ndate_str = dt_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ndate_datetime = datetime.datetime.strptime(ndate_str, "%Y-%m-%d %H:%M:%S")
        ndate_hour = ndate_datetime.hour
        ndate_day = ndate_datetime.day

        posts_in_ndate = pandas.concat([
            all_data_df.loc[(all_data_df[Structure.CREATION_TIME].dt.hour == ndate_hour) & (
                    all_data_df[Structure.CREATION_TIME].dt.day == ndate_day)]
        ])

        emotions_to_return[ndate_str] = {
            Responses.VALUE: len(posts_in_ndate),
            Responses.EMOTIONS: {}
        }
        for emotion in Emotions:
            emotions_to_return[ndate_str][Responses.EMOTIONS][emotion.value] = sum(posts_in_ndate[emotion.value])

    return emotions_to_return
