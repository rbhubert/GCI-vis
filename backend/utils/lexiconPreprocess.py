import os

import pandas
import pymongo
from nltk.corpus import wordnet
from nltk.stem import SnowballStemmer

# Preprocess the lexicon in the file lexicon.xlsx and saves it in the db.


DATABASE = "mongodb://localhost:27017/backend-g-TEST"
MONGODB_URI = os.environ.get('MONGODB_URI', DATABASE)
client = pymongo.MongoClient(MONGODB_URI)
db_name = MONGODB_URI.rsplit('/', 1)[-1]
db = client[db_name]
df = pandas.read_excel('lexicon.xlsx')
stemmer = SnowballStemmer('spanish')

all_entries = []

for index, row in df.iterrows():
    english = row["English"]
    synonyms = wordnet.synsets(english)
    if synonyms:
        synonyms = synonyms[0].lemma_names('spa')

    spanish = row["Spanish"].lower()
    synonyms.append(spanish)

    for word in synonyms:

        if word in all_entries:
            continue

        all_entries.append(word)
        stem = stemmer.stem(word)

        entry = {
            "english": english,
            "spanish": word,
            "stem": stem,
            "positive": row["Positive"],
            "negative": row["Negative"],
            "anger": row["Anger"],
            "anticipation": row["Anticipation"],
            "disgust": row["Disgust"],
            "fear": row["Fear"],
            "joy": row["Joy"],
            "sadness": row["Sadness"],
            "surprise": row["Surprise"],
            "trust": row["Trust"]
        }

        db["emotionLexicon"].insert_one(entry)
