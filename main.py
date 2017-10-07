# https://contest.yandex.ru/contest/5153/problems/B/

INSIDE = "INSIDE"
OUTSIDE = "OUTSIDE"
BORDER = "BORDER"
INPUT_FILENAME = "input.txt"
OUTPUT_FILENAME = "output.txt"
READ_MODE = "r"
WRITE_MODE = "w"
END_LINE = "\n"


def cmp_to_key(obj_cmp):
    """Convert a cmp= function into a key= function."""

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return obj_cmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return obj_cmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return obj_cmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return obj_cmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return obj_cmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return obj_cmp(self.obj, other.obj) != 0

    return K


class Point:
    """Represents a point on the (x,y) plane."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Compare points by its coordinates."""
        return self.x == other.x and self.y == other.y

    def is_inside_segment(self, segment_start_point, segment_finish_point):
        """
        Checks if point is inside segment,
        assuming that all 3 points lay on the same straight.
        """
        return segment_start_point.x < self.x < segment_finish_point.x or \
            segment_start_point.x > self.x > segment_finish_point.x or \
            segment_start_point.y < self.y < segment_finish_point.y or \
            segment_start_point.y > self.y > segment_finish_point.y or \
            segment_start_point == self or \
            segment_finish_point == self

    @staticmethod
    def get_rotation(a, b, c):
        """
        Gets rotation level by 3 points.
        If result is 0 - points lay on the same line,
        if result is > 0 - left rotation,
        if result is < 0 - right rotation.
        """
        return (b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x)


class Shape:
    """Represents a convex hull."""
    def __init__(self, points):
        """Initialize shape with array of points."""
        self.points = points

    def sort_points(self):
        """
        Sort points in counterclockwise order
        starting from first point in the array.
        """
        base = self.points[0]
        del self.points[0]
        self.points.sort(
            key=cmp_to_key(lambda x, y: Point.get_rotation(base, x, y)))
        self.points.insert(0, base)

    def is_point_inside(self, point):
        """
        Checks whether point lays inside the convex hull.
        Returns the position of the point: either INSIDE, OUTSIDE or BORDER.
        """

        # At first check if point lays inside the space,
        # limited by P_0-P_1 and P_0-P_N lines,
        # so the point will might lay inside the shape.
        # Also, checking if the point lays on the border of the shape.
        rotation_level_start_line = Point.get_rotation(
            self.points[0], self.points[1], point)
        if rotation_level_start_line == 0 and \
                point.is_inside_segment(self.points[0], self.points[1]):
            return BORDER
        rotation_level_finish_line = Point.get_rotation(
            self.points[0], self.points[len(self.points) - 1], point)
        if rotation_level_finish_line == 0 and point.is_inside_segment(
                self.points[0], self.points[len(self.points) - 1]):
            return BORDER

        if rotation_level_finish_line <= 0 <= rotation_level_start_line:
            return OUTSIDE

        # Using binary search find the smallest gap,
        # so the point might lay inside the space,
        # limited by P_0-left and P_0-right lines.
        left = 1
        right = len(self.points) - 1
        while right - left > 1:
            mid = (left + right) // 2
            if Point.get_rotation(self.points[0], self.points[mid], point) > 0:
                right = mid
            else:
                left = mid

        # Check if point lays inside the left-right segment.
        border_rotation = Point.get_rotation(
            self.points[left], self.points[right], point)
        if border_rotation == 0 and \
                point.is_inside_segment(self.points[left], self.points[right]):
            return BORDER

        # Check if P_0-point and left-right lines intersect.
        point_rotation = Point.get_rotation(
            self.points[0], point, self.points[left]) * \
            Point.get_rotation(self.points[0], point, self.points[right])
        border_rotation = Point.get_rotation(
            self.points[left], self.points[right], self.points[0]) * \
            Point.get_rotation(self.points[left], self.points[right], point)
        if point_rotation <= 0 and border_rotation > 0:
            return INSIDE
        return OUTSIDE


def read_points(stream):
    """
    Reads points from the input stream.
    Returns array of points.
    """
    points_count = int(stream.readline())
    points = []
    for i in range(points_count):
        x, y = map(int, stream.readline().split())
        points.append(Point(x, y))
    return points


def read_data(stream):
    """Reads points of the shape and queries."""
    return read_points(stream), read_points(stream)


def solve(points, queries):
    """
    Solves the problem.
    For each query returns if point is inside, outside or on border.
    """
    shape = Shape(points)
    shape.sort_points()

    answer = []
    for i in range(len(queries)):
        answer.append(shape.is_point_inside(queries[i]))
    return answer


def print_answer(stream, result):
    """Prints answer to the output stream."""
    for i in range(len(result)):
        stream.writelines(result[i] + END_LINE)

fin = open(INPUT_FILENAME, READ_MODE)
data = read_data(fin)
fin.close()

answer = solve(data[0], data[1])

fout = open(OUTPUT_FILENAME, WRITE_MODE)
print_answer(fout, answer)
fout.close()
