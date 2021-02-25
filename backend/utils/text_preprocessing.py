import re
import string

from emoji import UNICODE_EMOJI
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tokenizer import tokenizer

from enums import Token, TokenType
from enums.Emotions import Emotions
from utils.emotion_lexicon import emotionLexicon

# tweet tokenizer
# pip install git+https://github.com/erikavaris/tokenizer.git

is_number = re.compile(r'\d+(?:,\d*)?')
is_punctuation = re.compile(r"[{}]".format(string.punctuation + "¿¡"))

stop_words = stopwords.words('spanish')
stop_words.append("rt")

tweet_tokenizer = tokenizer.TweetTokenizer(preserve_url=False, preserve_case=False)
emotion_lexicon = emotionLexicon()


# This method will:
#   - split the text into tokens. This tokens will not be stopwords, urls or punctuation marks. Also, they will be in lower case.
#   - for each token, we will get the emotions related to it.
# Finally, we will have a list of tokens, each of them will have:
#   - its type, its value and its emotions (just a list of the enum.Emotions that have)

def split_text_twitter(text):
    tokens_w_stopwords_punctuation = tweet_tokenizer.tokenize(text)
    return __get_tokens_and_emotions(tokens_w_stopwords_punctuation)


def split_text_newspaper(text):
    tokens = word_tokenize(text)
    return __get_tokens_and_emotions(tokens)


def __get_tokens_and_emotions(unprocess_tokens):
    tokens = [token for token in unprocess_tokens if
              token not in stop_words and not is_punctuation.match(token) and not is_number.match(
                  token)]

    tokens_to_return = []

    for token in tokens:
        token_emotion = emotion_lexicon.get_emotion(token)
        emotions = []

        for emotion in Emotions:
            # if token_emotion.at[index, emotion.value]:
            if token_emotion[emotion.value] > 0:
                emotions.append(emotion.value)

        # Identification of the type of token...
        # If starts with # is a hashtag. If starts with @ is a mention.
        # If is in the UNICODE_EMOJI list, is a emoji.
        # Otherwise, its type is word.
        type_t = TokenType.WORD
        if token[0] == "#":
            type_t = TokenType.HASHTAG
        elif token[0] == "@":
            type_t = TokenType.MENTION
        elif token in UNICODE_EMOJI:
            type_t = TokenType.EMOJI

        new_token = {
            Token.TYPE: type_t,
            Token.VALUE: token,
            Token.EMOTIONS: emotions
        }
        tokens_to_return.append(new_token)

    return tokens_to_return
