import polars as pl
from modules.db import entities, db
import numpy as np
from sklearn.metrics import jaccard_score
import re
import json

PRIORITY_1_WEIGHT = 2
PRIORITY_2_WEIGHT = 1.5
SENIORITY_WEIGHT = 1.5

# The number of top mentors to return
TOP_K = 3


def create_jaccard_matrix(
    mentee_attribute_matrix: np.ndarray, mentor_attribute_matrix: np.ndarray
) -> list[tuple[int, list]]:
    jaccard_matrix: tuple[int, list] = []
    for l in range(len(mentee_attribute_matrix)):
        row_j = []
        for m in range(len(mentor_attribute_matrix)):
            value = jaccard_score(mentee_attribute_matrix, mentor_attribute_matrix[m])
            row_j.append(value)
        jaccard_matrix.append((l, row_j))
    return jaccard_matrix


# TODO: better name
def _check_if_in_generic_list(item, list: list[entities.GenericRow]):
    for i in list:
        if i.name == item:
            return 1
    return 0


def create_user_matrix(
    user: entities.ProfileUser,
    all_strengths: list[str],
    all_interests: list[str],
):
    # Attribute matrices
    strength_matrix = [
        (s["name"] in user["profile"]["strengths"]) for s in all_strengths
    ]
    interest_matrix = [
        (i["name"] in user["profile"]["interests"]) for i in all_interests
    ]

    user_matrix = np.concatenate(
        (
            strength_matrix,
            interest_matrix,
        ),
        # axis=1,
    )

    return user_matrix


def filter_by_first_priority(
    jaccard_matrix: list[tuple[int, list]],
    priority: str,
    mentors: list[entities.MentorUser],
):
    for i in range(len(jaccard_matrix)):
        if (
            # TODO: Is this correct?
            priority == mentors[i]["profile"]["first_priority"]
            or priority == entities.PreferenceType.no_preference.name
        ):
            jaccard_matrix[i] = (
                jaccard_matrix[i][0] * PRIORITY_1_WEIGHT,
                jaccard_matrix[i][1],
            )
    return jaccard_matrix


def filter_by_second_priority(
    jaccard_matrix: list[tuple[int, list]],
    priority: str,
    mentors: list[entities.MentorUser],
):
    for i in range(len(jaccard_matrix)):
        if (
            priority == mentors[i]["profile"]["second_priority"]
            or priority == entities.PreferenceType.no_preference.name
        ):
            jaccard_matrix[i] = (
                jaccard_matrix[i][0] * PRIORITY_2_WEIGHT,
                jaccard_matrix[i][1],
            )
    return jaccard_matrix


def _filter_by_preference(preference_type: entities.PreferenceType, a, b) -> bool:
    if preference_type == entities.PreferenceType.no_preference.name:
        return True

    return (a == b) and (preference_type == entities.PreferenceType.yes.name)


def filter_all_by_preference(
    user: entities.MenteeUser, mentors: list[entities.MentorUser]
) -> list[entities.MentorUser]:
    profile_filtered = list(
        filter(
            lambda x: (x["profile"] is not None),
            mentors,
        )
    )

    csap_track_filtered = list(
        filter(
            lambda x: (x["profile"]["csap_track"] == user["profile"]["csap_track"]),
            profile_filtered,
        )
    )

    same_theatre_filtered = list(
        filter(
            lambda x: _filter_by_preference(
                user["profile"]["same_theatre"],
                user["profile"]["theatre_id"],
                x["profile"]["theatre_id"],
            ),
            csap_track_filtered,
        )
    )

    same_gender_filtered = list(
        filter(
            lambda x: _filter_by_preference(
                user["profile"]["same_gender"],
                user["profile"]["gender"],
                x["profile"]["gender"],
            ),
            same_theatre_filtered,
        )
    )

    same_role_filtered = list(
        filter(
            lambda x: _filter_by_preference(
                user["profile"]["same_role"],
                user["profile"]["role_id"],
                x["profile"]["role_id"],
            ),
            same_gender_filtered,
        )
    )

    return same_role_filtered


seniority_regex_pattern = re.compile(
    r"\b(director|lead)\b", re.IGNORECASE | re.MULTILINE
)


def prioritise_by_seniority(
    jaccard_matrix: list[tuple[int, list, int]], mentors: list[entities.MentorUser]
):
    for i in range(len(jaccard_matrix)):
        if re.match(seniority_regex_pattern, mentors[i]["profile"]["title"]):
            jaccard_matrix[i] = (
                jaccard_matrix[i][0] * SENIORITY_WEIGHT,
                jaccard_matrix[i][1],
            )

    return jaccard_matrix


def match(
    user: entities.MenteeUser, mentors: list[entities.MentorUser]
) -> list[entities.MentorUser]:
    all_strengths = db.get_all_strengths()
    all_interests = db.get_all_interests()

    mentee_matrix = create_user_matrix(user, all_strengths, all_interests)

    partially_filtered_mentors = filter_all_by_preference(user, mentors)

    mentors_matrix = list(
        map(
            lambda x: create_user_matrix(x, all_strengths, all_interests),
            partially_filtered_mentors,
        )
    )

    jaccard_matrixes = list(
        map(
            lambda x: (
                jaccard_score(mentee_matrix, x[1]),
                partially_filtered_mentors[x[0]],
            ),
            enumerate(mentors_matrix),
        )
    )

    jaccard_matrixes = prioritise_by_seniority(jaccard_matrixes, mentors)

    jaccard_matrixes = filter_by_first_priority(
        jaccard_matrixes, user["profile"]["first_priority"], mentors
    )

    jaccard_matrixes = filter_by_second_priority(
        jaccard_matrixes, user["profile"]["second_priority"], mentors
    )

    jaccard_matrixes = sorted(jaccard_matrixes, key=lambda x: x[0], reverse=True)

    return list(map(lambda x: x[1], jaccard_matrixes))[:TOP_K]
