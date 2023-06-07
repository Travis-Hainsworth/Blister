""""
Input:
m_axle = The y position values of the axle marker
m_rim_top = The y position values of the top of the rim marker

Output:
radial_compression = The smoothed values of the radial compression throughout the test
"""
import math


def calc_radial_compression(m_axle, m_rim_top):

    radial_vector = m_axle - m_rim_top
    radial_length = math.sqrt(sum(radial_vector**2, 2))
    radial_compression = radial_length - radial_length[1]

    radial_compression.rolling(50).mean()

