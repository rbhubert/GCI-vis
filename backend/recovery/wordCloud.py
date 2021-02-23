import pandas

from enums import Token, TokenType
from enums.dbStructure import Structure, NewspaperStructure, Post


# Returns the valid words for a wordcloud. This means that there are no stopwords and punctuation signs.
# It returns the words, and the frequency and the emotions associated with each one.
def get_wordCloud_socialMedia(posts):
    all_words = []
    for post in posts:
        all_words.extend([
            {"text": token[Token.VALUE],
             "emotions": token[Token.EMOTIONS]} for token in
            post[Structure.POST][Post.SPLITTED]
            if token[Token.TYPE] == TokenType.WORD or token[Token.TYPE] == TokenType.HASHTAG
        ])

    return get_frequent_words(all_words, posts.count())


# Returns the valid words for a wordcloud. This means that there are no stopwords and punctuation signs.
# It returns the words, and the frequency and the emotions associated with each one.
def get_wordCloud_newspaper(comments):
    list_words = []
    for comment in comments:
        list_words.extend([
            {"text": token[Token.VALUE],
             "emotions": token[Token.EMOTIONS]} for token in
            comment[NewspaperStructure.Comments.TEXT]
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
