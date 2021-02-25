import pandas

from enums import Responses
from enums.Emotions import Emotions
from enums.dbStructure import Structure
from utils.get_emotions import get_emotions_social_media
from utils.utils_date import daterange


# Returns the value of the interaction in the entry
def interaction_values(entry, interaction):
    i_value = entry[Structure.INTERACTIONS][interaction]
    if isinstance(i_value, list):
        return len(i_value)
    elif isinstance(i_value, dict):
        return sum(i_value.values())
    else:
        return i_value


# For each date in daterange(_posts_), returns:
#   - number of tweets,
#   - the hashtags used on those tweets,
#   - the ids of those tweets,
#   - the interactions values received
#   - the emotions values associated to those tweets
def get_activity(posts, structure_interaction):
    posts_df = pandas.DataFrame(list(posts))
    emotions_column = []
    for index, post in posts_df.iterrows():
        emotions_column.append(get_emotions_social_media(post))

    posts_df[Structure.EMOTIONS] = emotions_column

    for emotion in Emotions:
        posts_df[emotion.value] = posts_df[Structure.EMOTIONS].apply(lambda x: x.get(emotion.value, 0))

    for interaction in structure_interaction:
        posts_df[interaction] = posts_df.apply(
            lambda entry: interaction_values(entry, interaction), axis=1)

    min_date = posts_df[Structure.CREATION_TIME].min()
    max_date = posts_df[Structure.CREATION_TIME].max()

    activity_to_return = {}

    for dt in daterange(min_date, max_date):
        ndate = dt.strftime("%Y-%m-%d")
        posts_in_ndate = posts_df.loc[pandas.to_datetime(posts_df[Structure.CREATION_TIME].dt.date) == ndate]

        posts_with_hashtags_ndate = posts_in_ndate[posts_in_ndate[Structure.HASHTAGS].map(lambda d: len(d)) > 0]
        hashtags_ndate = {}
        if not posts_with_hashtags_ndate.empty:
            hashtags_ndate = posts_with_hashtags_ndate[Structure.HASHTAGS].apply(pandas.Series).stack().reset_index(
                drop=True)
            hashtags_ndate = hashtags_ndate.groupby(hashtags_ndate).count().to_dict()

        activity_to_return[ndate] = {
            Responses.VALUE: len(posts_in_ndate),
            Responses.HASHTAGS: hashtags_ndate,
            Responses.TWEETSID: posts_in_ndate[Structure.ID].tolist(),
            Responses.INTERACTIONS: {},
            Responses.EMOTIONS: {}
        }

        for emotion in Emotions:
            activity_to_return[ndate][Responses.EMOTIONS][emotion.value] = int(posts_in_ndate[emotion.value].sum())

        for interaction in structure_interaction:
            activity_to_return[ndate][Responses.INTERACTIONS][interaction] = int(posts_in_ndate[interaction].sum())

    return activity_to_return
