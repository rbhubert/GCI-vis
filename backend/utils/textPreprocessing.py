import re
import string

from emoji import UNICODE_EMOJI
from nltk.corpus import stopwords
from tokenizer import tokenizer

from enums import Token, TokenType
from enums.Emotions import Emotions
from utils.emotionLexicon import emotionLexicon

isNumber = re.compile(r'\d+(?:,\d*)?')
isPunctuation = re.compile(r"[{}]".format(string.punctuation + "¿¡"))

stop_words = stopwords.words('spanish')
stop_words.append("rt")

Tokenizer = tokenizer.TweetTokenizer(preserve_url=False, preserve_case=False)
emLe = emotionLexicon()


# This method will:
#   - split the text into tokens. This tokens will not be stopwords, urls or punctuation marks. Also, they will be in lower case.
#   - for each token, we will get the emotions related to it.
# Finally, we will have a list of tokens, each of them will have:
#   - its type, its value and its emotions (just a list of the enum.Emotions that have)

def split_text(text):
    tokens_w_stopwords_punctuation = Tokenizer.tokenize(text)

    tokens = [token for token in tokens_w_stopwords_punctuation if
              # token not in stop_words and token not in punctuation and not isNumber.match(token)]
              token not in stop_words and not isPunctuation.match(token) and not isNumber.match(token)]

    tokens_to_return = []

    for token in tokens:
        token_emotion = emLe.getEmotion(token)
        index = token_emotion.index.item()
        emotions = []

        for emotion in Emotions:
            if token_emotion.at[index, emotion.value]:
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
