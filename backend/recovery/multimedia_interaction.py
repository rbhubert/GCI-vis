from itertools import combinations

import pandas

from enums import Responses
from enums.dbStructure import Structure


# Returns True only if there is no multimedia resource use in the _entry_
def is_only_text(entry, structure_multimedia):
    for multimedia in structure_multimedia:
        if entry[multimedia] > 0:
            return False

    return True


# Returns True only if there is no interaction in the _entry_
def no_interaction(entry, structure_interaction):
    for interaction in structure_interaction:
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
def at_least_one(entry, combinations):
    for combination in combinations:
        if entry[combination]:
            return True

    return False


# Returns True only if exists _interaction_ in _entry_
def interaction_values(entry, interaction):
    i_value = entry[Structure.INTERACTIONS][interaction]
    if isinstance(i_value, list):
        return len(i_value) > 0
    elif isinstance(i_value, dict):
        return any(v > 0 for v in i_value.values())
    else:
        return i_value > 0


def only_multimedia(df, multimedia, structure_multimedia):
    sum_multimedia = 0
    for multi in structure_multimedia:
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
def get_multimedia_interaction(structure_multimedia, structure_interaction, posts):
    posts_df = pandas.DataFrame(list(posts))

    for multimedia in structure_multimedia:
        posts_df[multimedia] = posts_df[Structure.MULTIMEDIA].apply(
            lambda x: len(x.get(multimedia, 0)) > 0)

    posts_df[Responses.TEXT] = posts_df.apply(
        lambda row: is_only_text(row, structure_multimedia), axis=1)

    for interaction in structure_interaction:
        posts_df[interaction] = posts_df.apply(
            lambda entry: interaction_values(entry, interaction), axis=1)

    posts_df[Responses.NONE] = posts_df.apply(
        lambda row: no_interaction(row, structure_interaction), axis=1)

    multimedia_interaction_to_return = {
        Responses.TOTAL: posts.count(),
        Responses.TEXT: {
            Responses.TOTAL: len(posts_df.loc[posts_df[Responses.TEXT]]),
            Responses.NONE: len(posts_df.loc[(posts_df[Responses.TEXT]) & (posts_df[Responses.NONE])])
        }
    }

    for multimedia in structure_multimedia:
        multimedia_interaction_to_return[multimedia] = {
            Responses.TOTAL: only_multimedia(posts_df, multimedia, structure_multimedia),
            Responses.NONE: len(posts_df.loc[(posts_df[multimedia]) & (posts_df[Responses.NONE])])
        }
        sum_interactions = 0
        for interaction in structure_interaction:
            mi_value = len(posts_df.loc[(posts_df[multimedia]) & (posts_df[interaction])])
            multimedia_interaction_to_return[multimedia][interaction] = mi_value
            sum_interactions += mi_value

        if sum_interactions == 0:
            sum_interactions = 1

        for interaction in structure_interaction:
            mi_value = multimedia_interaction_to_return[multimedia][interaction]
            multimedia_interaction_to_return[multimedia][interaction] = (multimedia_interaction_to_return[multimedia][
                                                                             Responses.TOTAL] -
                                                                         multimedia_interaction_to_return[multimedia][
                                                                             Responses.NONE]) * (
                                                                                mi_value / sum_interactions)

    sum_interactions = 0
    for interaction in structure_interaction:
        mi_value = len(posts_df.loc[(posts_df[Responses.TEXT]) & (posts_df[interaction])])
        multimedia_interaction_to_return[Responses.TEXT][interaction] = mi_value
        sum_interactions += mi_value

    if sum_interactions == 0:
        sum_interactions = 1

    for interaction in structure_interaction:
        mi_value = multimedia_interaction_to_return[Responses.TEXT][interaction]
        multimedia_interaction_to_return[Responses.TEXT][interaction] = (multimedia_interaction_to_return[
                                                                             Responses.TEXT][
                                                                             Responses.TOTAL] -
                                                                         multimedia_interaction_to_return[
                                                                             Responses.TEXT][
                                                                             Responses.NONE]) * (
                                                                                mi_value / sum_interactions)
    return multimedia_interaction_to_return


# Structures the relation between the multimedia resources use
# -
# Determines the number of tweets...
#   - using x multimedia resource (_structureMultimedia enum_)
#   - using more than a multimedia resource simultaneously
def get_multimedia(structure_multimedia, posts):
    posts_df = pandas.DataFrame(list(posts))

    for multimedia in structure_multimedia:
        posts_df[multimedia] = posts_df[Structure.MULTIMEDIA].apply(
            lambda x: True if len(x.get(multimedia, 0)) else False)

    multimedia_combinations = sum(
        [list(map(list, combinations(structure_multimedia, i))) for i in range(1, len(structure_multimedia) + 1)], [])

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
def get_interaction(structure_interaction, posts):
    posts_df = pandas.DataFrame(list(posts))

    for interaction in structure_interaction:
        posts_df[interaction] = posts_df.apply(
            lambda entry: interaction_values(entry, interaction), axis=1)

    posts_df[Responses.TOTAL] = posts_df.apply(
        lambda entry: at_least_one(entry, structure_interaction), axis=1)

    interaction_comb = sum(
        [list(map(list, combinations(structure_interaction, i))) for i in range(1, len(structure_interaction) + 1)], [])

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
