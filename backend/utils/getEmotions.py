import pandas

from enums.Emotions import Emotions
from enums.dbStructure import Structure, Post


# Returns the emotions associated to the _post_. If is not a comment, it counts the emotions in each of its comments.
def get_emotions(post, smStructure, iscomment):
    if iscomment:
        sentiments = __get_emotions(post)
    else:
        sentiments = {}
        comments = post[smStructure.INTERACTIONS][smStructure.Interactions.COMMENTS]
        comments_sentiments = [comment[smStructure.EMOTIONS] for comment in comments]

        datafram = pandas.DataFrame(comments_sentiments)

        for emot in Emotions:
            sentiments[emot.value] = 0 if datafram.empty else datafram[emot.value].sum().item()

    return sentiments


# Returns the emotions of the comment _post_
def __get_emotions(post):
    post_text = post[Structure.POST][Post.SPLITTED]

    words = pandas.DataFrame({
        "emotions": [x["emotions"] for x in post_text]
    })

    sentiments = {}

    for emot in Emotions:
        mask = words.emotions.apply(lambda x: emot.value in x)
        sentiments[emot.value] = len(words[mask])

    return sentiments


def get_emotions_newItem(comments):
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


def get_emotions_comment(comment):
    comment_text = comment["text"]

    words = pandas.DataFrame({
        "emotions": [x["emotions"] for x in comment_text]
    })

    emotions = {}
    for emot in Emotions:
        mask = words.emotions.apply(lambda x: emot.value in x)
        emotions[emot.value] = len(words[mask])

    return emotions
