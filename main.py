from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from logging import getLogger, basicConfig

from Vector import element

LOG_FORMAT = "[%(asctime)s, %(levelname)s], [%(filename)s, %(funcName)s, %(lineno)s]: %(message)s"
basicConfig(filename=None, level=50, format=LOG_FORMAT)
logger = getLogger()
getLogger('matplotlib.font_manager').disabled = True


p1 = element.Point(logger)
p2 = element.Point(logger)
p3 = element.Point(logger)

p1.from_polar(0, 0, 0)
p2.from_polar(1, 0, 50)
p3.from_polar(1, 10, 45)


v1 = element.Vector(logger, p1, p2)
v2 = element.Vector(logger, p2, p3)

v3 = v1 + v2


line1 = v1.as_plt()
line2 = v2.as_plt()
line3 = v3.as_plt()

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot(line1[0], line1[1], line1[2], label='parametric curve', marker="o")
ax.plot(line2[0], line2[1], line2[2], label='parametric curve', marker="o")
ax.plot(line3[0], line3[1], line3[2], label='parametric curve', marker="o")
ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

print(v1.angle_between(v2))

plt.show()

