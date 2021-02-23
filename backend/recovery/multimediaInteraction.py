from itertools import combinations

import pandas

from enums import Responses
from enums.dbStructure import Structure


# Returns True only if there is no multimedia resource use in the _entry_
def isOnlyText(entry, structureMultimedia):
    for multimedia in structureMultimedia:
        if entry[multimedia] > 0:
            return False

    return True


# Returns True only if there is no interaction in the _entry_
def noInteraction(entry, structureInteraction):
    for interaction in structureInteraction:
        if entry[interaction] > 0:
            return False

    return True


# Returns True only if the _entry_ uses each
#  --multimedia resource --interactions
#  of the _combinations_ list
def simultaneously(entry, combinations):
    for combination in combinations:
        if not entry[combination]:
            return False

    return True


# Returns True only if the _entry_ uses al least one of the
#  --multimedia resource --interactions
#  of the _combinations_ list
def atLeastOne(entry, combinations):
    for combination in combinations:
        if entry[combination]:
            return True

    return False


# Returns True only if exists _interaction_ in _entry_
def interactionValues(entry, interaction):
    iValue = entry[Structure.INTERACTIONS][interaction]
    if isinstance(iValue, list):
        return len(iValue) > 0
    elif isinstance(iValue, dict):
        return any(v > 0 for v in iValue.values())
    else:
        return iValue > 0


def onlyMultimedia(df, multimedia, structureMultimedia):
    sum_multimedia = 0
    for multi in structureMultimedia:
        if multi != multimedia:
            sum_multimedia += len(df.loc[(df[multi]) & (df[multimedia])])

    return len(df.loc[df[multimedia]]) - sum_multimedia


# Structures the relation between multimedia resources use and the possible interactions received
# -
# For each tweet using a given multimedia resource, it counts how many of them has each interaction
# with value greater than zero -> then determines the percentage
#
# Determines the number of tweets...
# - using x multimedia resource (_structureMultimedia enum_)
#       - and the percentage of these tweets
#         receiving z interaction (_structureInteraction enum_)
# - using no-multimedia resource (only text)
#       - and the percentage of these tweets
#         receiving z interaction (_structureInteraction enum_)
def get_multimediaInteraction(structureMultimedia, structureInteraction, posts):
    posts_df = pandas.DataFrame(list(posts))

    for multimedia in structureMultimedia:
        posts_df[multimedia] = posts_df[Structure.MULTIMEDIA].apply(
            lambda x: len(x.get(multimedia, 0)) > 0)

    posts_df[Responses.TEXT] = posts_df.apply(
        lambda row: isOnlyText(row, structureMultimedia), axis=1)

    for interaction in structureInteraction:
        posts_df[interaction] = posts_df.apply(
            lambda entry: interactionValues(entry, interaction), axis=1)

    posts_df[Responses.NONE] = posts_df.apply(
        lambda row: noInteraction(row, structureInteraction), axis=1)

    multimediaInteraction_to_return = {
        Responses.TOTAL: posts.count(),
        Responses.TEXT: {
            Responses.TOTAL: len(posts_df.loc[posts_df[Responses.TEXT]]),
            Responses.NONE: len(posts_df.loc[(posts_df[Responses.TEXT]) & (posts_df[Responses.NONE])])
        }
    }

    for multimedia in structureMultimedia:
        multimediaInteraction_to_return[multimedia] = {
            Responses.TOTAL: onlyMultimedia(posts_df, multimedia, structureMultimedia),
            Responses.NONE: len(posts_df.loc[(posts_df[multimedia]) & (posts_df[Responses.NONE])])
        }
        sum_interactions = 0
        for interaction in structureInteraction:
            mi_value = len(posts_df.loc[(posts_df[multimedia]) & (posts_df[interaction])])
            multimediaInteraction_to_return[multimedia][interaction] = mi_value
            sum_interactions += mi_value

        if sum_interactions == 0:
            sum_interactions = 1

        for interaction in structureInteraction:
            mi_value = multimediaInteraction_to_return[multimedia][interaction]
            multimediaInteraction_to_return[multimedia][interaction] = (multimediaInteraction_to_return[multimedia][
                                                                            Responses.TOTAL] -
                                                                        multimediaInteraction_to_return[multimedia][
                                                                            Responses.NONE]) * (
                                                                               mi_value / sum_interactions)

    sum_interactions = 0
    for interaction in structureInteraction:
        mi_value = len(posts_df.loc[(posts_df[Responses.TEXT]) & (posts_df[interaction])])
        multimediaInteraction_to_return[Responses.TEXT][interaction] = mi_value
        sum_interactions += mi_value

    if sum_interactions == 0:
        sum_interactions = 1

    for interaction in structureInteraction:
        mi_value = multimediaInteraction_to_return[Responses.TEXT][interaction]
        multimediaInteraction_to_return[Responses.TEXT][interaction] = (multimediaInteraction_to_return[Responses.TEXT][
                                                                            Responses.TOTAL] -
                                                                        multimediaInteraction_to_return[Responses.TEXT][
                                                                            Responses.NONE]) * (
                                                                               mi_value / sum_interactions)
    return multimediaInteraction_to_return


# Structures the relation between the multimedia resources use
# -
# Determines the number of tweets...
#   - using x multimedia resource (_structureMultimedia enum_)
#   - using more than a multimedia resource simultaneously
def get_multimedia(structureMultimedia, posts):
    posts_df = pandas.DataFrame(list(posts))

    for multimedia in structureMultimedia:
        posts_df[multimedia] = posts_df[Structure.MULTIMEDIA].apply(
            lambda x: True if len(x.get(multimedia, 0)) else False)

    multimedia_combinations = sum(
        [list(map(list, combinations(structureMultimedia, i))) for i in range(1, len(structureMultimedia) + 1)], [])

    for multimedia in multimedia_combinations:
        if len(multimedia) < 2:
            continue

        text = '_'.join(multimedia)
        posts_df[text] = posts_df.apply(
            lambda row: simultaneously(row, multimedia), axis=1)

    multimedia_to_return = []

    for multimedia in multimedia_combinations:
        text = '_'.join(multimedia)
        m_value = len(posts_df.loc[(posts_df[text])])
        multimedia_to_return.append({
            Responses.SETS: multimedia,
            Responses.SIZE: m_value
        })

    return multimedia_to_return


# Structures the possible interactions from users
# -
# Determines the number of tweets...
#   - that received at least one interaction
#   - that received x interaction (_structureInteraction enum_)
#   - that received more than a interaction simultaneously
def get_interaction(structureInteraction, posts):
    posts_df = pandas.DataFrame(list(posts))

    for interaction in structureInteraction:
        posts_df[interaction] = posts_df.apply(
            lambda entry: interactionValues(entry, interaction), axis=1)

    posts_df[Responses.TOTAL] = posts_df.apply(
        lambda entry: atLeastOne(entry, structureInteraction), axis=1)

    interaction_comb = sum(
        [list(map(list, combinations(structureInteraction, i))) for i in range(1, len(structureInteraction) + 1)], [])

    interaction_combinations = [[Responses.TOTAL]]
    interaction_combinations.extend(interaction_comb)

    for interaction in interaction_combinations:
        if len(interaction) < 2:
            continue

        text = '_'.join(interaction)
        posts_df[text] = posts_df.apply(
            lambda row: simultaneously(row, interaction), axis=1)

    interactions_to = []

    for interaction in interaction_combinations:
        text = '_'.join(interaction)
        i_value = len(posts_df.loc[(posts_df[text])])
        interactions_to.append({
            Responses.SETS: interaction,
            Responses.SIZE: i_value
        })

    interaction_to_return = {
        Responses.SETS: interactions_to
    }
    return interaction_to_return
