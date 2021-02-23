import pandas

from enums import Responses
from enums.Emotions import Emotions
from enums.dbStructure import Structure
from utils.utilsDate import daterange


# Returns the value of the interaction in the entry
def interactionValues(entry, interaction):
    iValue = entry[Structure.INTERACTIONS][interaction]
    if isinstance(iValue, list):
        return len(iValue)
    elif isinstance(iValue, dict):
        return sum(iValue.values())
    else:
        return iValue


# For each date in daterange(_posts_), returns:
#   - number of tweets,
#   - the hashtags used on those tweets,
#   - the ids of those tweets,
#   - the interactions values received
#   - the emotions values associated to those tweets
def get_activity(posts, structureInteraction):
    posts_df = pandas.DataFrame(list(posts))

    for emotion in Emotions:
        posts_df[emotion.value] = posts_df[Structure.EMOTIONS].apply(lambda x: x.get(emotion.value, 0))

    for interaction in structureInteraction:
        posts_df[interaction] = posts_df.apply(
            lambda entry: interactionValues(entry, interaction), axis=1)

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

        for interaction in structureInteraction:
            activity_to_return[ndate][Responses.INTERACTIONS][interaction] = int(posts_in_ndate[interaction].sum())

    return activity_to_return
