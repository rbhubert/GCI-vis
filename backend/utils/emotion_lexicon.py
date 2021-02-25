import pandas
from nltk.stem import SnowballStemmer

# from database.database import LexiconDB
from enums.Emotions import Emotions
from utils.singleton import Singleton

# Stemmer for spanish words
stemmer = SnowballStemmer('spanish')


# Singleton class for access to lexicon
class emotionLexicon(metaclass=Singleton):
    def __init__(self):
        self.dfLexicon = pandas.read_excel("./utils/lexicon.xlsx")
        self.dfLexicon.rename(columns={"spanish": "word"}, inplace=True)
        self.dfLexicon["stem"] = self.dfLexicon["word"].apply(lambda word: stemmer.stem(word))

    # Returns the emotions associated to the _word_.
    # First it checks if the word is in the dataFrame (entries). If is not, searches the word in the lexiconDB and adds
    # the information in the dataFrame.
    def get_emotion(self, word):
        stem = stemmer.stem(word)
        result = self.dfLexicon[self.dfLexicon["word"] == word]
        if result.empty:
            result = self.dfLexicon[self.dfLexicon["stem"] == stem]
            if result.empty:
                result = {
                    "word": word
                }
                for em in Emotions:
                    result[em.value] = 0

                self.dfLexicon = self.dfLexicon.append(result, ignore_index=True)

        if not isinstance(result, dict):
            result = result.iloc[0].to_dict()

        return result
