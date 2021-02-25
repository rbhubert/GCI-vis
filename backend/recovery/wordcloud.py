import pandas

from enums import Token, TokenType
from enums.dbStructure import Structure, NewspaperStructure
from utils.text_preprocessing import split_text_newspaper


# Returns the valid words for a wordcloud. This means that there are no stopwords and punctuation signs.
# It returns the words, and the frequency and the emotions associated with each one.
def get_wordcloud_social_media(posts):
    all_words = []
    for post in posts:
        tokens = post[Structure.POST][Structure.Post.SPLITTED]

        all_words.extend([
            {"text": token[Token.VALUE],
             "emotions": token[Token.EMOTIONS]} for token in
            tokens
            if
            token[Token.TYPE] == TokenType.WORD or token[Token.TYPE] == TokenType.HASHTAG
        ])

    return get_frequent_words(all_words, posts.count())


# Returns the valid words for a wordcloud. This means that there are no stopwords and punctuation signs.
# It returns the words, and the frequency and the emotions associated with each one.
def get_wordcloud_newspaper(comments):
    list_words = []
    for comment in comments:
        tokens = split_text_newspaper(comment[NewspaperStructure.Comments.TEXT])
        list_words.extend([
            {"text": token[Token.VALUE],
             "emotions": token[Token.EMOTIONS]} for token in
            tokens
            if token[Token.TYPE] == TokenType.WORD or token[Token.TYPE] == TokenType.HASHTAG
        ])
    if not list_words:  # is empty
        return "Error"  # TODO error message

    return get_frequent_words(list_words, len(comments))


# Return the most frequent words > those words that appear in the corpus more frequently that a threshold.
# This threshold is calculated based on the maximum frequency identified in the corpus, the total number of
# posts/comments and the total number of words.
def get_frequent_words(list_words, total_posts):
    # create a dataframe from all_words. Get the frequency of the words by grouping by word. Remove duplicates
    words = pandas.DataFrame(list_words)
    words["size"] = words.groupby(["text"])["text"].transform("size")
    words = words.drop_duplicates(["text"])

    max_frequency = words.loc[words["size"].idxmax()]["size"]
    percentage_threshold = (100 * total_posts) / words.shape[0]
    size_threshold = (percentage_threshold * max_frequency) / 100

    # get only the rows that have frequency higher than size_threshold
    words_to_return = words.loc[words['size'] >= size_threshold]
    return words_to_return.to_dict(orient="records")
