import pandas

from enums import Token
from enums.Emotions import Emotions
from enums.dbStructure import Structure
from utils.text_preprocessing import split_text_twitter, split_text_newspaper


# Returns the emotions associated to the _post_. If is not a comment, it counts the emotions in each of its comments.
def get_emotions_social_media(post):
    sentiments = {}
    comments = post[Structure.INTERACTIONS][Structure.Interactions.COMMENTS]
    comments_sentiments = [__get_emotions_comment(comment) for comment in comments]

    dataframe = pandas.DataFrame(comments_sentiments)

    for emot in Emotions:
        sentiments[emot.value] = 0 if dataframe.empty else dataframe[emot.value].sum().item()

    return sentiments


# Returns the emotions of the comment _post_
def __get_emotions_comment(post):
    tokens = post[Structure.POST][Structure.Post.SPLITTED]
    words = pandas.DataFrame({
        "emotions": [x[Token.EMOTIONS] for x in tokens]
    })

    sentiments = {}

    for emot in Emotions:
        mask = words.emotions.apply(lambda x: emot.value in x)
        sentiments[emot.value] = len(words[mask])

    return sentiments


def get_emotions_news_item(comments):
    # for each comment in comments
    # for each reply in comment
    # sum every emotion
    emotions = {}

    all_comments_and_replies = pandas.DataFrame(comments)

    if all_comments_and_replies.empty:
        for emot in Emotions:
            emotions[emot.value] = 0
        return emotions

    for comm in comments:
        for rep in comm["replies"]:
            all_comments_and_replies = all_comments_and_replies.append(rep, ignore_index=True)

    for emotion in Emotions:
        all_comments_and_replies[emotion.value] = all_comments_and_replies[Structure.EMOTIONS].apply(
            lambda x: x.get(emotion.value, 0))
    all_data_df = all_comments_and_replies.sum()

    for emot in Emotions:
        emotions[emot.value] = int(all_data_df[emot.value])

    return emotions


def get_emotions_news_comment(comment):
    comment_text = comment["text"]
    tokens = split_text_newspaper(comment_text)

    words = pandas.DataFrame({
        "emotions": [x[Token.EMOTIONS] for x in tokens]
    })

    sentiments = {}

    for emot in Emotions:
        mask = words.emotions.apply(lambda x: emot.value in x)
        sentiments[emot.value] = len(words[mask])

    return sentiments
