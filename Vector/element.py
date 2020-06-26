import math


class Vector:
    def __init__(self, logger, start_point, end_point):
        self.logger = logger
        if isinstance(start_point, Point):
            self.start_point = start_point
        else:
            self.start_point = Point(self.logger)

        if isinstance(end_point, Point):
            self.end_point = end_point
        else:
            self.end_point = Point(self.logger)

    def __str__(self):
        return "Vector({}, {})".format(self.start_point, self.end_point)

    def __add__(self, other):
        return self.add(other, override=False)

    def __neg__(self):
        return Vector(self.logger, self.end_point, self.start_point)

    def __sub__(self, other):
        return self.subtract(other, override=False)

    def __mul__(self, other):
        return self.multiply(other, override=False)

    def __truediv__(self, scalar):
        return self.divide(scalar, override=False)

    def __eq__(self, other):
        self.is_same(other)

    def mag(self):
        self.logger.info("Calling Point.dist")
        return self.end_point.dist(self.start_point)

    def is_same(self, other):
        return self.start_point == other.start_point and self.end_point == other.end_point

    def dot(self, other):
        if isinstance(other, Vector):
            diff_point_me = self.end_point - self.start_point
            diff_point_other = other.end_point - self.start_point

            return diff_point_me.x * diff_point_other.x + diff_point_me.y * diff_point_other.y + diff_point_me.z * diff_point_other.z

        else:
            self.logger.error("Unsupported type")
            raise ValueError("Unsupported type")

    def multiply(self, other, override=True):
        self.logger.info("Calculating {} * {}".format(self, other))
        new_start_point = self.start_point
        if isinstance(other, (int, float)):
            endpoint_from_zero = self.end_point - self.start_point
            new_end_point = self.start_point + endpoint_from_zero * other
        elif isinstance(other, Vector):
            from_zero_me = self.end_point - self.start_point
            from_zero_other = other.end_point - self.start_point

            new_end_point = Point(self.logger,
                                  x=from_zero_me.y * from_zero_other.z - from_zero_me.z * from_zero_other.y,
                                  y=from_zero_me.z * from_zero_other.x - from_zero_me.x * from_zero_other.z,
                                  z=from_zero_me.x * from_zero_other.y - from_zero_me.y * from_zero_other.x)

            new_end_point = self.start_point + new_end_point
        else:
            self.logger.error("Unsupported type")
            raise ValueError("Unsupported type")

        if override:
            self.start_point = new_start_point
            self.end_point = new_end_point
        else:
            return Vector(self.logger, new_start_point, new_end_point)

    def divide(self, other, override=False):
        self.logger.info("Calling Vector.multiply")
        if isinstance(other, (int, float)):
            if override:
                self.multiply(1 / other, override=override)
            else:
                return self.multiply(1 / other, override=override)
        elif isinstance(other, Vector):
            self.logger.error("Vector by Vector division is not possible")
            raise ValueError("Vector by Vector division is not possible")
        else:
            self.logger.error("Unsupported type")
            raise ValueError("Unsupported type")

    def add(self, other, override=True):
        self.logger.info("Calculating {} + {}".format(self, other))
        diff_other = other.start_point - self.end_point
        new_end_point = other.end_point - diff_other
        if override:
            self.end_point = new_end_point
        else:
            return Vector(self.logger, self.start_point, new_end_point)

    def subtract(self, other, override=True):
        self.logger.info("Calling Vector.add")
        if override:
            self.add(-other, override=override)
        else:
            return self.add(-other, override=override)

    def heading(self):
        self.logger.info("Calculating Heading")
        if not self.start_point == self.end_point:
            r = self.mag()
            phi = math.acos((self.end_point.z - self.start_point.z) / r)
            theta = math.atan2((self.end_point.y - self.start_point.y), (self.end_point.x - self.start_point.x))
            return math.radians(theta), math.radians(phi)

        self.logger.error("{} is not a valid vector".format(self))
        raise ValueError("{} is not a valid vector".format(self))

    def unit(self):
        self.logger.info("Calculating unit vector of {}".format(self))
        if not self.start_point.is_same(self.end_point):
            m = self.mag()

            new_end_point = self.end_point - self.start_point

            return Vector(self.logger, self.start_point, new_end_point / m)

        self.logger.error("{} is not a valid vector".format(self))
        raise ValueError("{} is not a valid vector".format(self))

    def as_plt(self):
        return [[self.start_point.x, self.end_point.x],
                [self.start_point.y, self.end_point.y],
                [self.start_point.z, self.end_point.z]]

    def angle_between(self, other):
        self.logger.info("calculating angle between {} and {}".format(self, other))
        if isinstance(other, Vector):
            diff_other = other.start_point - self.start_point
            new_end_point = other.end_point - diff_other
            new_v = Vector(self.logger, self.start_point, new_end_point)
            return math.degrees(math.acos(self.dot(new_v) / (self.mag() * new_v.mag())))
        else:
            self.logger.error("Unsupported type")
            raise ValueError("Unsupported type")


class Point:
    def __init__(self, logger, x=0, y=0, z=0):
        self.logger = logger
        if isinstance(x, (int, float)):
            self.x = float(x)
        else:
            self.x = 0

        if isinstance(y, (int, float)):
            self.y = float(y)
        else:
            self.y = 0

        if isinstance(z, (int, float)):
            self.z = float(z)
        else:
            self.z = 0

    def __str__(self):
        return "Point(x={}, y={}, z={})".format(self.x, self.y, self.z)

    def __sub__(self, other):
        return self.subtract(other, override=False)

    def __add__(self, other):
        return self.add(other, override=False)

    def __neg__(self):
        return Point(self.logger, x=-self.x, y=-self.y, z=-self.z)

    def __mul__(self, scalar):
        return self.scale(scalar, override=False)

    def __truediv__(self, scalar):
        return self.divide(scalar, override=False)

    def __eq__(self, other):
        return self.is_same(other)

    def dist(self, other=None):
        self.logger.info("Calculating distance between {} and {}".format(self, other))
        if other is None:
            other = Point(0, 0, 0)

        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2) +
                         math.pow(self.z - other.z, 2))

    def is_same(self, other):
        self.logger.info("Checking if {} and {} are same points".format(self, other))
        return self.x == other.x and self.y == other.y and self.z == other.z

    def from_polar(self, r, theta, phi, override=True):
        self.logger.info("Calculating polar to cartesian")
        if r == 0:
            x, y, z = 0, 0, 0
        else:
            theta = math.radians(theta)
            phi = math.radians(phi)

            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)

        if override:
            self.x, self.y, self.z = x, y, z
        else:
            return Point(self.logger, x=x, y=y, z=z)

    def add(self, other, override=True):
        self.logger.info("Calculating {} + {}".format(self, other))

        if isinstance(other, Point):
            new_x = self.x + other.x
            new_y = self.y + other.y
            new_z = self.z + other.z

        else:
            self.logger.error("Data must be a Point")
            raise ValueError("Data must be a Point")

        if override:
            self.x = new_x
            self.y = new_y
            self.z = new_z
        else:
            return Point(self.logger, x=new_x, y=new_y, z=new_z)

    def subtract(self, other, override=True):
        self.logger.info("Calling Point.add")
        if override:
            self.add(-other, override=override)
        else:
            return self.add(-other, override=override)

    def scale(self, scalar, override=True):
        self.logger.info("Scaling the {}".format(self))

        if isinstance(scalar, (int, float)):
            new_x = self.x * scalar
            new_y = self.y * scalar
            new_z = self.z * scalar
        else:
            self.logger.error("Scalar must be float or int")
            raise ValueError("Scalar must be float or int")

        if override:
            self.x, self.y, self.z = new_x, new_y, new_z
        else:
            return Point(self.logger, x=new_x, y=new_y, z=new_z)

    def divide(self, scalar, override=True):
        self.logger.info("Calling Point.scale")
        if isinstance(scalar, int) or isinstance(scalar, float):
            if override:
                self.scale(1 / scalar, override=override)
            else:
                return self.scale(1 / scalar, override=override)
        else:
            self.logger.error("Divider must be float or int")
            raise ValueError("Divider must be float or int")

    def to_polar(self):
        if self.x == self.y == self.z == 0:
            return 0, 0, 0
        self.logger.info("Converting from cartesian to polar")
        r = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))
        phi = math.atan2(self.y, self.x)
        theta = math.acos(self.z / r)
        return r, math.degrees(theta), math.degrees(phi)
    
