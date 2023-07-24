import math


def calculate_suspension_travel(front_travel, rear_travel):
    switch_cases = {
        0 < front_travel < 74: 1,
        74 <= front_travel < 88: 2,
        88 <= front_travel < 102: 3,
        102 <= front_travel < 116: 4,
        116 <= front_travel < 130: 5,
        130 <= front_travel < 144: 6,
        144 <= front_travel < 158: 7,
        158 <= front_travel < 172: 8,
        172 <= front_travel < 186: 9,
        front_travel >= 186: 10
    }

    front_suspension = switch_cases[True]

    switch_cases = {
        0 < rear_travel < 74: 1,
        74 <= rear_travel < 88: 2,
        88 <= rear_travel < 102: 3,
        102 <= rear_travel < 116: 4,
        116 <= rear_travel < 130: 5,
        130 <= rear_travel < 144: 6,
        144 <= rear_travel < 158: 7,
        158 <= rear_travel < 172: 8,
        172 <= rear_travel < 186: 9,
        rear_travel >= 186: 10
    }

    rear_suspension = switch_cases[True]

    avg_travel = (front_suspension + rear_suspension) / 2

    return math.floor(avg_travel)


def calculate_weight(rider_weight):
    switch_cases = {
        0 < rider_weight < 96: 1,
        96 <= rider_weight < 112: 2,
        112 <= rider_weight < 128: 3,
        128 <= rider_weight < 144: 4,
        144 <= rider_weight < 160: 5,
        160 <= rider_weight < 176: 6,
        176 <= rider_weight < 192: 7,
        192 <= rider_weight < 208: 8,
        208 <= rider_weight < 224: 9,
        rider_weight >= 224: 10
    }

    return switch_cases[True]


def calculate_finesse_environment(rider_finesse_power, trail_environment):
    finesse_environment = ((.08 * trail_environment * rider_finesse_power) + .8)

    return finesse_environment


def calculate_regression_deformation(rider_weight, rider_aggression, finesse_environment, avg_travel):
    regression = .993 * ((.0533 * rider_weight) +
                         (.0326 * rider_aggression) +
                         (.0205 * finesse_environment) +
                         (.008 * avg_travel) - .112)

    return regression


def calculate_regression_energy(rider_weight, rider_aggression, finesse_environment, avg_travel):
    regression = .9465 * ((.0176 * rider_weight) +
                          (.0473 * rider_aggression) +
                          (.0329 * finesse_environment) +
                          (.0235 * avg_travel) - .117)

    return regression
