import math

Point2D = tuple[int, int]


def get_orientation(p: Point2D, q: Point2D, r: Point2D):
    """Return >0 if counter-clockwise, <0 if clockwise, 0 if collinear"""

    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def distance2(p: Point2D, q: Point2D):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def get_convex_hull(
    points: list[Point2D],
    include_collinear: bool = False,
) -> list[Point2D]:
    """
    Construct the convex hull of a set of points using Graham's scan
    algorithm.

    Returns the points in counter-clockwise order starting from the
    leftmost point.

    Warning: This function modifies the input list of points.
    """

    # Remove duplicates
    points = list(set(points))

    if len(points) <= 2:
        return points

    # Step 1: Find the bottom-most point (and leftmost if tie)
    p0 = min(points, key=lambda p: (p[1], p[0]))
    points.remove(p0)

    # Step 2: Sort points by polar angle with respect to p0
    points.sort(
        key=lambda p: (
            math.atan2(p[1] - p0[1], p[0] - p0[0]),
            distance2(p0, p),
        )
    )

    # Step 3: Process sorted points to build convex hull
    hull: list[Point2D] = [p0]
    for pt in points:
        while len(hull) >= 2:
            orientation = get_orientation(hull[-2], hull[-1], pt)
            if orientation > 0 or (include_collinear and orientation == 0):
                break
            hull.pop()
        hull.append(pt)

    return hull


while True:
    n = int(input())
    if n == 0:
        break

    points: list[Point2D] = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))

    sol = get_convex_hull(points)
    print(len(sol))
    for point in sol:
        print(point[0], point[1])
