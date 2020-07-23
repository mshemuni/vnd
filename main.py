
from Vector import Point, Vector

p1 = Point([1, 2, 3])
p2 = Point([1, 5, 7])

# p1.from_polar({"r": 10, "phi": 45, "thetas":[90, 10]})
# p2.from_polar({"r": 10, "phi": 135, "thetas":[90, 10]})
# print(p1)
# print(p2)

# print(p1 + p2)

v1 = Vector(p1)
v2 = Vector(p2)

print(v1.cross(v2))
