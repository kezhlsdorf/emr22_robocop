#!/usr/bin/env python3
# =================================================
# edited WHS, OJ , 2.6.2023 #
#
# ArUco Marker in einem Bild/Pdf erstellen
# https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/aruco_basics.html
#

from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl


aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)

fig = plt.figure()
nx = 1  # Spalten nebeneinander
ny = 1  # Reihen übereinander
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny, nx, i)
    img = aruco.drawMarker(aruco_dict, i, 700)
    plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")

plt.savefig("/home/oj/Bilder/aruco.png")
plt.show()
