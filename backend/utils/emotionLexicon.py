import pandas
from nltk.stem import SnowballStemmer

from database.database import LexiconDB
from enums.Emotions import Emotions
from utils.singleton import Singleton

# Stemmer for spanish words
stemmer = SnowballStemmer('spanish')


# Singleton class for access to lexicon. Serves as a "cache" using a DataFrame
class emotionLexicon(metaclass=Singleton):
    def __init__(self):
        self.dbLexicon = LexiconDB()
        columns = ["word"]
        for em in Emotions:
            columns.append(em.value)
        self.entries = pandas.DataFrame(columns=columns)

    # Returns the emotions associated to the _word_.
    # First it checks if the word is in the dataFrame (entries). If is not, searchs the word in the lexiconDB and adds
    # the information in the dataFrame.
    def getEmotion(self, word):
        if word not in self.entries.word.values:
            stem = stemmer.stem(word)
            entry_raw = self.dbLexicon.get_lexicon(word, stem)

            entry = {
                "word": word
            }

            for em in Emotions:
                entry[em.value] = entry_raw[em.value] if entry_raw is not None else 0

            self.entries = self.entries.append(entry, ignore_index=True)

        return self.entries[
            self.entries['word'] == word]  # .values[0]  to access only to the values such as ['vivo' 0 0 0 0 1 0 0 0]
