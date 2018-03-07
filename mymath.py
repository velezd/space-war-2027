from math import asin, degrees, sqrt


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """ Return True if the values a and b are close to each other and False otherwise.

    :param a: first value
    :param b: second value
    :param rel_tol: maximum allowed difference between a and b, relative to the larger absolute value of a or b
    :param abs_tol: minimum absolute tolerance
    :return: True/False
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def rt_angle(a, b):
    """ Calculates angle alpha from sides a and b in right triangle where gama is 90 deg

    :param a: Side a
    :param b: Side b
    :return: Angle alpha
    """
    return degrees(asin(a / sqrt(a ** 2 + b ** 2)))
