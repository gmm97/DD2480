from ctypes import util
from email import utils
import math
import numpy as np
from utils import *


def cmv_condition_0(point_array, length1):
    """
    Checks if there is a set of consecutive data points
        with a distance greater than a set length apart

    Args:
        point_array (type: list of 2-tuples): contains (x,y) values
        length1 (type: float): minimum distance necessary

    Returns:
        (type: boolean) True if condition met, false otherwise
    """
    if len(point_array) < 2:
        return False
    for i in range(len(point_array) - 1):
        if distance_between_points(point_array[i], point_array[i + 1]) > length1:
            return True
    return False


def cmv_condition_1(points, radius):
    """
    Returns true if there exists at least one set of three consecutive data points that cannot all be contained
    within or on a circle of given radius.

    Args:
        point_array (type: list of 2-tuples): contains (x,y) values
        radius (type: float): radius of the circle

    Returns:
        (type: boolean) True if condition met, false otherwise"""
    if len(points) < 3:
        return False
    for i in range(len(points) - 2):
        p1, p2, p3 = points[i], points[i + 1], points[i + 2]
        center = calculate_center([p1, p2, p3])
        if (
            distance_exceeds_radius(p1, center, radius)
            or distance_exceeds_radius(p2, center, radius)
            or distance_exceeds_radius(p3, center, radius)
        ):
            return True
    return False


def cmv_condition_2(points, epsilon):
    """
    There exists at least one set of three consecutive data
        points that form an angle greater than pi + epsilon or less tha npi - epsilon

    Args:
        points (list): coordinates
        epsilon (float): angle

    Returns:
        True if condition is satisfied, false otherwise
    """

    # returns the angle formed by the line segments p1 -> p2 -> p3
    def get_angle(p1, p2, p3):  # p1, p2, p3 are points
        v12 = distance_between_points(p1, p2)
        v23 = distance_between_points(p2, p3)
        v31 = distance_between_points(p3, p1)
        return math.acos((v12**2 + v23**2 - v31**2) / (2 * v12 * v23))

    for i in range(len(points) - 2):
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2]

        if p1 == p2 or p2 == p3:
            continue

        angle = get_angle(p1, p2, p3)
        if angle < math.pi - epsilon or angle > math.pi + epsilon:
            return True
    return False


def cmv_condition_3(points, area1):
    """
    There exists at least one set of three consecutive data
        points that are the vertices of a triangle
        with area greater than AREA1. (0 ≤ AREA1)

    Args:
        points (list): coordinates
        area1 (float): area of a triangle

    Returns:
        True if a traingle with greater area than AREA1 exists
    """
    if len(points) < 3:
        return False
    total_points = len(points)
    for i in range(total_points - 2):
        area = calculate_area_triangle(points[i], points[i + 1], points[i + 2])
        if area >= area1:
            return True
    return False


def check_condition_4(point_array, Q_PTS, quad):
    """Checks if There exists at least one set of Q PTS consecutive data points that lie in more than QUADS
    quadrants.
    """

    def number_of_quad(points):
        in_quads = [0, 0, 0, 0]
        for pt in points:
            if pt[0] >= 0 and pt[1] >= 0:
                in_quads[0] = 1
            elif pt[0] < 0 and pt[1] >= 0:
                in_quads[1] = 1
            elif pt[0] <= 0 and pt[1] < 0:
                in_quads[2] = 1
            elif pt[0] > 0 and pt[1] < 0:
                in_quads[3] = 1

        return sum(in_quads)

    if len(point_array) < Q_PTS:
        return False
    for i in range(len(point_array) - Q_PTS + 1):
        if number_of_quad(point_array[i : i + Q_PTS]) >= quad:
            return True

    return False


def check_condition_5(point_array):
    """
    Checks if there are two consecutive x-coords such that
        the first subtracted from the second is less than 0

    Args:
        point_array (type: list of 2-tuples): contains (x,y) values

    Returns:
        (type: boolean) True if condition met, false otherwise
    """
    if len(point_array) < 2:
        return False
    for i in range(len(point_array) - 1):
        if point_array[i + 1][0] - point_array[i][0] < 0:
            return True
    return False


def cmv_condition_6(points, N_PTS, dist):
    """
    Checks if there exists at least one set of N PTS consecutive data points such that at least one of the
    points lies a distance greater than DIST from the line joining the first and last of these N PTS
    points.

    Args:
        point_array (type: list of 2-tuples): contains (x,y) values
        N_PTS (type: int): Number of consecutive data points
        dist: cut-off distance between the first and last of N_PTS

    Returns:
        (type: boolean) True if condition met, false otherwise
    """
    if len(points) < 3 or len(points) < N_PTS:
        return False
    for beginIdx in range(len(points) - N_PTS + 1):
        endIdx = beginIdx + N_PTS - 1
        beginPoint, endPoint = points[beginIdx], points[endIdx]
        # Same begin and end point, return True if distance of middle points from beginPoint > dist
        if beginPoint == endPoint:
            for midIdx in range(beginIdx + 1, endIdx):
                midPoint = points[midIdx]
                if distance_between_points(midPoint, beginPoint) > dist:
                    return True
        # different begin and end point, calculate distance from midpoint to line formed
        else:
            beginPoint, endPoint = np.asarray(beginPoint), np.asarray(endPoint)
            for midIdx in range(beginIdx + 1, endIdx):
                midPoint = np.asarray(points[midIdx])
                distance_from_line = np.abs(
                    np.cross(beginPoint - endPoint, endPoint - midPoint)
                ) / np.linalg.norm(beginPoint - endPoint)
                if distance_from_line > dist:
                    return True
    return False


def cmv_condition_7(points, K_PTS, length1):
    """
    Checks if there are two points p1, p2, in the array seperated by K_PTS conscutive
    intervening points, and the distance between p1 and p2 is greater than length1

    Args:
        points (type: list of 2-tuples): contains (x,y) values
        K_PTS (type: int): number of intervening points
        length1 (type: float): minimum distance necessary

    Returns:
        (type: boolean) True if condition met, False, otherwise
    """

    if len(points) < 3:
        return False

    for i in range(len(points) - K_PTS - 1):
        p1 = points[i]
        p2 = points[i + K_PTS + 1]
        if distance_between_points(p1, p2) > length1:
            return True
    return False


def cmv_condition_8(points, a_pts, b_pts, radius1, numpoints):
    """
    There exists at least one set of three data points separated by exactly
    A PTS and B PTS consecutive intervening points, respectively, that cannot
    be contained within or on a circle of radius RADIUS1.

    The condition is not met when NUMPOINTS < 5.
    1≤A PTS,1≤B PTS
    A PTS+B PTS ≤ (NUMPOINTS−3)

    Args:
        points (list): coordinates
        a_pts (int): number of interevening points
        b_pts (int): number of inttervening points
        radius1 (float): circle radius

    Returns:
        True if conditions are met
    """
    if numpoints < 5:
        return False

    for i in range(numpoints - a_pts - b_pts - 2):
        p1 = points[i]
        p2 = points[i + a_pts + 1]
        p3 = points[i + a_pts + b_pts + 2]
        center = calculate_center([p1, p2, p3])
        if (
            distance_exceeds_radius(p1, center, radius1)
            or distance_exceeds_radius(p2, center, radius1)
            or distance_exceeds_radius(p3, center, radius1)
        ):
            return True
    # Both conditions failed
    return False


def check_condition_9(point_array, C_PTS, D_PTS, epsilon):
    """Check if there exists at least one set of three data points separated by exactly C PTS and D PTS
    consecutive intervening points, respectively, that form an angle such that:
    angle < (PI−EPSILON)
        or
    angle > (PI+EPSILON)
    """

    if len(point_array) < 5:
        return False

    for i in range(len(point_array) - C_PTS - 1 - D_PTS - 1):
        if (
            point_array[i] == point_array[i + C_PTS + 1]
            or point_array[i + C_PTS + 1] == point_array[i + C_PTS + 1 + D_PTS + 1]
        ):
            continue
        angle = calculate_angle_between_points(
            point_array[i],
            point_array[i + C_PTS + 1],
            point_array[i + C_PTS + 1 + D_PTS + 1],
        )
        if angle < math.pi - epsilon or angle > math.pi + epsilon:
            return True
    return False


def cmv_condition_10(point_array, e_pts, f_pts, area1, num_points):
    """Checks if there is a set of three data points, separated by
        e_pts and f_pts respectively, that form a triangle with an
        area greater than area1

    Args:
        point_array (list of 2-tuples): contains (x,y) values
        e_pts (int): amount of steps separating first and second vertex
        f_pts (int): amount of steps separating second and third vertex
        area1 (double): area which triangle must be larger than
        num_points (int): amount of points in the point_array

    Returns:
        (boolean): True if condition met, false otherwise
    """
    if num_points < 5:
        return False

    for i in range(len(point_array)):
        if i + e_pts + 1 + f_pts + 1 >= num_points:  # looped as far as possible
            break
        # use triangle coord formula
        area = calculate_area_triangle(
            point_array[i],
            point_array[i + e_pts + 1],
            point_array[i + e_pts + 1 + f_pts + 1],
        )
        if area > area1:
            return True
    return False


def cmv_condition_11(points, G_PTS):
    """
    Checks if there exists at least one set of two data points, (X[i],Y[i]) and (X[j],Y[j]), separated by
    exactly G PTS consecutive intervening points, such that X[j] - X[i] < 0. (where i < j )

    Args:
        points (type: list of 2-tuples): contains (x,y) values
        G_PTS (type: int): number of intervening points

    Returns:
        (type: boolean) True if condition met, False, otherwise
    """
    if G_PTS > len(points) - 2 or len(points) < 3:
        return False
    for beginIdx in range(len(points) - G_PTS - 1):
        endIdx = beginIdx + G_PTS + 1
        x_begin, x_end = points[beginIdx][0], points[endIdx][0]
        if x_end - x_begin < 0:
            return True
    return False


def cmv_condition_12(points, K_PTS, length1, length2):
    """
    Checks if there are two points separated by K_PTS intervening points that are > length1 apart
    as well as two points separated by K_PTS intervening points that are < length2 apart

    Args:
        points (type: list of 2-tuples): contains (x,y) values
        K_PTS (type: int): number of intervening points
        length1 (type: float): minimum distance necessary
        length2 (type: float): maximum distance between points
    """

    for i in range(len(points) - K_PTS - 1):
        p1 = points[i]
        p2 = points[i + K_PTS + 1]
        if distance_between_points(p1, p2) < length2:
            return True and cmv_condition_7(points, K_PTS, length1)
    return False


def cmv_condition_13(points, a_pts, b_pts, radius1, radius2, numpoints):
    """
    There exists at least one set of three data points, separated by exactly A PTS and B PTS
    consecutive intervening points, respectively, that cannot be contained within or on a
    circle of radius RADIUS1. In addition, there exists at least one set of three data points
    (which can be the same or different from the three data points just mentioned)
    separated by exactly A PTS and B PTS consecutive intervening points, respectively,
    that can be contained in or on a circle of radius RADIUS2.
    Both parts must be true for the LIC to be true.
    The condition is not met when NUMPOINTS < 5.


    Args:
        points (list): list of (x,y) coordinates
        a_pts (int): number of intervening points
        b_pts (int): number of intervening points
        radius1 (float): circle radius
        radius2 (float): circle radius, must be 0 ≤ RADIUS2

    Returns:
        True if conditions are met
    """
    if numpoints < 5:
        return False

    for i in range(numpoints - a_pts - b_pts - 2):
        p1 = points[i]
        p2 = points[i + a_pts + 1]
        p3 = points[i + a_pts + b_pts + 2]

        # Same as calculations as cmv_1
        center = calculate_center([p1, p2, p3])

        if (
            not distance_exceeds_radius(p1, center, radius2)
            and not distance_exceeds_radius(p2, center, radius2)
            and not distance_exceeds_radius(p3, center, radius2)
        ):
            return cmv_condition_8(points, a_pts, b_pts, radius1, numpoints)

    return False


def check_condition_14(point_array, E_PTS, F_PTS, area1, area2):
    """Check if:
    (1) there exists at least one set of three data points, separated by exactly
        E PTS and F PTS consecutive intervening points, respectively, that are
        the vertices of a triangle with area greater than AREA1.
    (2) there exist three data points separated by exactly E PTS and F PTS consecutive
        intervening points, respectively, that are the vertices of a triangle with area
        less than AREA2.
    """

    if len(point_array) < 5:
        return False

    conditions = [False, False]

    for i in range(len(point_array) - E_PTS - 1 - F_PTS - 1):
        area = calculate_area_triangle(
            point_array[i],
            point_array[i + E_PTS + 1],
            point_array[i + E_PTS + 1 + F_PTS + 1],
        )
        if area >= area1:
            conditions[0] = True
        if area <= area2:
            conditions[1] = True
        if conditions[0] and conditions[1]:
            return True
    return False


if __name__ == "__main__":
    pass
