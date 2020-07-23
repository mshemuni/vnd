from logging import getLogger

import numpy as np


class Point:
    def __init__(self, points=None, logger=None):
        self.logger = logger or getLogger("dummy")
        self.points = points or [0, 0, 0]
        self.points = np.array(self.points)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # From https://github.com/allelos/vectors/blob/master/vectors/vectors.py
        return "{}({})".format(self.__class__.__name__, ", ".join(list(map(str, self.points))))

    def __neg__(self):
        # Changes all values sgins
        return Point(points=list(-self.points), logger=self.logger)

    def __add__(self, other):
        # Call self.add on a + b
        return self.add(other)

    def __sub__(self, other):
        # Call self.subtract on a - b
        return self.subtract(other)

    def __mul__(self, scalar):
        # Call self.scale on a * b
        return self.scale(scalar)

    def __rmul__(self, scalar):
        # Call self.scale on a * b
        return self.scale(scalar)

    def __truediv__(self, scalar):
        # Call self.divide on a / b
        return self.divide(scalar)

    def __eq__(self, other):
        # Call self.is_same on a == b
        return self.is_same(other)

    def __len__(self):
        # Returns number of elements
        return self.points.size

    def copy(self):
        """Returns a copy of vector"""
        self.logger.info("Copying Vector")
        return Point(points=list(self.points.copy()), logger=self.logger)

    def dist(self, other=None):
        """Calculates distance from origin or a given point"""
        self.logger.info("Calculating distance")
        if other is None:
            other = np.zeros(len(self.points))
        return np.sqrt(
            np.power(self.points - other, 2).sum()
        )

    def to_polar(self):
        """Converts cartesian to polar"""
        self.logger.info("Converting to polar")
        # From http://www.avidsynergy.com/pdf/n_dimensional_spherical_cordinates.pdf
        r = self.dist()
        thetas = [np.rad2deg(np.arccos(self.points[0] / r))]
        for point in self.points[1: -2]:
            thetas.append(
                np.rad2deg(
                    np.arccos(
                        point / (r * np.prod(np.sin(np.deg2rad(thetas))))
                    )
                )
            )

        phi = np.rad2deg(
            np.arccos(
                self.points[-2] / (r * np.prod(np.sin(np.deg2rad(thetas))))
            )
        )

        return {"r": r, "phi": phi, "thetas": thetas}

    def from_polar(self, coordinate, override=True):
        """Converts polar to cartesian"""
        self.logger.info("Converting to cartesian")
        r = coordinate["r"]
        phi = np.deg2rad(coordinate["phi"])
        thetas = np.deg2rad(coordinate["thetas"])

        points = [r * np.cos(thetas[0])]
        thetas_for_sins = [thetas[0]]
        for theta in thetas[1:]:
            points.append(r * np.prod(np.sin(thetas_for_sins)) * np.cos(theta))
            thetas_for_sins.append(theta)

        points.append(r * np.prod(np.sin(thetas_for_sins)) * np.cos(phi))
        points.append(r * np.prod(np.sin(thetas_for_sins)) * np.sin(phi))

        if override:
            self.points = np.array(points)

        return Point(points=points, logger=self.logger)

    def add(self, other):
        """Adds two points"""
        self.logger.info("Calculating {} + {}".format(self, other))
        if isinstance(other, Point):
            if len(self) == len(other):
                return Point(points=list(self.points + other.points), logger=self.logger)
            else:
                self.logger.error("Two points must have same dimension number")
                raise ValueError("Two points must have same dimension number")
        else:
            self.logger.error("Data must be a Point type")
            raise ValueError("Data must be a Point type")

    def subtract(self, other):
        """Subtracts two points"""
        self.logger.info("Calling {}.add".format(self.__class__.__name__))
        return self.add(-other)

    def scale(self, scalar):
        """Scales a point with a scalar"""
        self.logger.info("Scaling {} with {}".format(self, scalar))
        if isinstance(scalar, (int, float)):
            return Point(points=list(self.points * scalar), logger=self.logger)
        else:
            self.logger.error("Scalar must be float or int type")
            raise ValueError("Scalar must be float or int type")

    def divide(self, scalar):
        """Divides a point with a scalar"""
        self.logger.info("Calling {}.scale".format(self.__class__.__name__))
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return self.scale(1 / scalar)

    def is_same(self, other):
        """Checking if two vectors are same"""
        self.logger.info("Checking if {} and {} are same".format(self, other))
        if isinstance(other, Point):
            return (self.points == other.points).all()
        else:
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")


class Vector:
    def __init__(self, point=None, logger=None):
        self.logger = logger or getLogger("dummy")
        self.point = point or Point(logger=self.logger)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # From https://github.com/allelos/vectors/blob/master/vectors/vectors.py
        return "{}({})".format(self.__class__.__name__, self.point)

    def __neg__(self):
        return Vector(point=-self.point, logger=self.logger)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __rmul__(self, other):
        return self.multiply(other)

    def __truediv__(self, scalar):
        return self.divide(scalar)

    def __abs__(self):
        return self.mag()

    def __len__(self):
        return len(self.point)

    def __eq__(self, other):
        return self.is_same(other)

    def cross(self, other):
        """Cross product fo two vector"""
        self.logger.info("Calculating {} * {}".format(self, other))
        if isinstance(other, Vector):
            if other.point.points.size == self.point.points.size:
                return np.cross(self.point.points, other.point.points)
            else:
                self.logger.error("Two points must share same dimension number")
                raise ValueError("Two points must share same dimension number")
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_same(self, other):
        """Checking if two vectors are same"""
        self.logger.info("Checking if {} and {} are same".format(self, other))
        if isinstance(other, Vector):
            return self.point == other.point
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def from_points(self, point1, point2, override=True):
        """Creates a vector from two points"""
        self.logger.info("Creating a vector from {} and {}".format(point1, point2))
        if isinstance(point1, Point) and isinstance(point2, Point):
            diff = point1 - point2
            if override:
                self.point = diff
            else:
                return Vector(point=diff, logger=self.logger)
        else:
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    def copy(self):
        """Copies a vector"""
        self.logger.info("Creating a copy")
        return Vector(point=self.point.copy(), logger=self.logger)

    def dot(self, other):
        """Calculates dot product"""
        self.logger.info("Calculating {}.{}".format(self, other))
        if isinstance(other, Vector):
            if other.point.points.size == self.point.points.size:
                return np.dot(other.point.points, self.point.points)
            else:
                self.logger.error("Two points must share same dimension number")
                raise ValueError("Two points must share same dimension number")
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def multiply(self, other):
        """Multiplies two vectors"""
        self.logger.info("Calculating {} * {}".format(self, other))
        if isinstance(other, (int, float)):
            return Vector(point=self.point * other, logger=self.logger)
        elif isinstance(other, Vector):
            if len(self) == len(other):
                points = []
                for point in other.point.points:
                    points.append((point * self.point.points).sum())

                return Vector(point=Point(points=points, logger=self.logger), logger=self.logger)
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def divide(self, scalar):
        """Scales a vector"""
        self.logger.info("Calculating {} / {}".format(self, scalar))
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ValueError("Cannot divide by zero")

            return self.multiply(1 / scalar)
        elif isinstance(scalar, Vector):
            self.logger.error("Vector by Vector division is not possible")
            raise ValueError("Vector by Vector division is not possible")
        else:
            self.logger.error("Data must be numeric type")
            raise ValueError("Data must be numeric type")

    def mag(self):
        """Calculates Magnitude of vector"""
        self.logger.info("Calculating magnitude")
        return self.point.dist()

    def add(self, other):
        """Adds two vectors"""
        self.logger.info("Calculating {} + {}".format(self, other))
        if isinstance(other, Vector):
            if len(self) == len(other):
                return Vector(self.point + other.point, logger=self.logger)
            else:
                self.logger.error("Two points must have same dimension number")
                raise ValueError("Two points must have same dimension number")
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def subtract(self, other):
        """Subtracts two vectors"""
        self.logger.info("Calculating {} - {}".format(self, other))
        return self.add(-other)

    def heading(self):
        """Calculates heading direction"""
        self.logger.info("Calculating heading")
        jacobian = self.point.to_polar()
        return {"phi": jacobian["phi"], "thetas": jacobian["thetas"]}

    def unit(self):
        """Calculates unit vector"""
        self.logger.info("Calculating unit vector")
        return self / self.mag()

    def angle_between(self, other):
        """calculates angle between two vectors"""
        self.logger.info("Calculating angle between {} and {}".format(self, other))
        if isinstance(other, Vector):
            if len(self) == len(other):
                if other.unit() == self.unit():
                    return {"phi": 0, "thetas": [0]*(len(self) - 2)}
                else:
                    return np.rad2deg(self.dot(other) / (self.mag() * other.mag()))
            else:
                self.logger.error("Two points must have same dimension number")
                raise ValueError("Two points must have same dimension number")
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_perpendicular(self, other):
        if isinstance(other, Vector):
            return self.dot(other) == 0
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

