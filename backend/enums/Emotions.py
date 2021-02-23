from enum import Enum


# Enum of the possible emotions that can be found in one text post.
# Based on the Plutchik's wheel of emotions.
class Emotions(Enum):
    ANGER = "anger"
    ANTICIPATION = "anticipation"
    DISGUST = "disgust"
    FEAR = "fear"
    JOY = "joy"
    SADNESS = "sadness"
    SURPRISE = "surprise"
    TRUST = "trust"


# Enum with the midpoint for each pair of emotions on the wheel
class EmotionsMiddle(Enum):
    ANGER_DISGUST = "anger-disgust"
    ANTICIPATION_ANGER = "anticipation-anger"
    DISGUST_SADNESS = "disgust-sadness"
    FEAR_TRUST = "fear-trust"
    JOY_ANTICIPATION = "joy-anticipation"
    SADNESS_SURPRISE = "sadness-surprise"
    SURPRISE_FEAR = "surprise-fear"
    TRUST_JOY = "trust-joy"
