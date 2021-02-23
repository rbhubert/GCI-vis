import datetime

import pandas

from enums import Responses
from enums.Emotions import Emotions, EmotionsMiddle
from enums.dbStructure import Structure
from utils.utilsDate import daterange, daterange_hours


# Returns the emotions and combinations between them associated with the _posts_
def get_emotionsCombinations_socialMedia(posts):
    return __create_RadarDataframe(list(posts))


# Returns the emotions and combinations between them associated with the _comments_ to a newspaper
def get_emotionsCombinations_newspaper(comments):
    return __create_RadarDataframe(list(comments))


# Creates Dataframe from the list _posts_ and calculates the size of each emotions related
# to the posts.
def __create_RadarDataframe(posts):
    emotions_to_return = {
        Responses.EMOTIONS: {},
        Responses.KEYS: []
    }

    all_data_df = pandas.DataFrame(posts)
    for emotion in Emotions:
        all_data_df[emotion.value] = all_data_df[Structure.EMOTIONS].apply(lambda x: x.get(emotion.value, 0))
    all_data_df = all_data_df.sum()
    i_aux = ""
    for emotion in Emotions:
        emotions_to_return[Responses.KEYS].append(emotion.value)
        emotions_to_return[Responses.EMOTIONS][emotion.value] = int(all_data_df[emotion.value])
        emotions_to_return[Responses.EMOTIONS][i_aux] = 0
        i_aux += " "

    i_aux = ""
    for emotion in EmotionsMiddle:
        emotions = emotion.value.split("-")
        dataEmot = [emotions_to_return[Responses.EMOTIONS][emotions[0]],
                    emotions_to_return[Responses.EMOTIONS][emotions[1]]]
        emotions_to_return[Responses.EMOTIONS][i_aux] = (emotions_to_return[Responses.EMOTIONS][emotions[0]] +
                                                         emotions_to_return[Responses.EMOTIONS][emotions[1]]) / 2
        i_aux += " "

    return emotions_to_return


# Returns the emotions associated with the _posts_
def get_emotions_socialMedia(posts):
    return __create_BubbleDataframe(list(posts))


# Returns the emotions associated with the _comments_ to a news.
def get_emotions_newspaper(comments):
    return __create_BubbleDataframe_newspaper(list(comments))


# Creates a Dataframe from the list _posts_ and identifies the dates and the number of comments and
# the emotions associated with that date.
def __create_BubbleDataframe(posts):
    all_data_df = pandas.DataFrame(posts)

    for emotion in Emotions:
        all_data_df[emotion.value] = all_data_df[Structure.EMOTIONS].apply(lambda x: x.get(emotion.value, 0))

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
def __create_BubbleDataframe_newspaper(posts):
    all_data_df = pandas.DataFrame(posts)

    for emotion in Emotions:
        all_data_df[emotion.value] = all_data_df[Structure.EMOTIONS].apply(lambda x: x.get(emotion.value, 0))

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
