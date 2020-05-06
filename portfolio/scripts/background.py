import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def create_background():
    # - Figure and Axes - #
    fig, ax = plt.subplots(figsize=(12.8, 9.6)); ax.set_axis_off()
    fig.subplots_adjust(left=0., right=1., top=1., bottom=0.)
    ax.set_xlim((0.2, 0.8)); ax.set_ylim((0.2, 0.8))

    # - Delauney Triangulation - #
    points = np.random.rand(200, 2)
    X, Y = points.T
    tri = Delaunay(points)
    ax.triplot(X, Y, tri.simplices.copy(), alpha=0.5, c="w", lw=0.5)

    # - Triangle polygons - #
    triangles = points[tri.simplices.copy()]
    polygons = [Polygon(xy) for xy in triangles]
    p = PatchCollection(polygons, alpha=0.4, match_original=False)

    # - Add with colors - #
    colors = np.sqrt(np.sum(np.square(triangles.mean(axis=1)), axis=1))
    p.set_clim(-0.3, 1.3)

    p.set_array(colors)
    ax.add_collection(p)

    fig.savefig("static/images/background.png", dpi=400)

def create_background_gradient():
    # - Figure and Axes - #
    fig, ax = plt.subplots(figsize=(12.8/2, 9.6/2)); ax.set_axis_off()
    fig.subplots_adjust(left=0., right=1., top=1., bottom=0.)
    ax.set_xlim((0.2, 0.8)); ax.set_ylim((0.2, 0.8))

    # - Delauney Triangulation - #
    points = np.random.rand(200, 2)
    X, Y = points.T
    tri = Delaunay(points)
    ax.triplot(X, Y, tri.simplices.copy(), alpha=0.5, c="w", lw=0.5)

    # - Triangle polygons - #
    triangles = points[tri.simplices.copy()]
    polygons = []
    for xy in triangles:
        x_mid = np.mean(xy, axis=0)
        for factor in np.logspace(-2., 1., 20):
            xyi = xy + factor*(x_mid-xy)
            polygons.append(Polygon(xyi))

    # polygons = [Polygon(xy, zorder=np.random.uniform(0, 100)) for xy in triangles]
    p = PatchCollection(polygons, alpha=0.01, match_original=False)

    # - Add with colors - #
    colors = np.sqrt(np.sum(np.square(triangles.mean(axis=1)), axis=1))
    colors = np.repeat(colors, 20)
    p.set_clim(-0.3, 1.3)
    p.set_array(colors)
    ax.add_collection(p)
if __name__=="__main__":
    create_background()