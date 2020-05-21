import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def subplots_axis_off(**kwargs):
    fig, ax = plt.subplots(**kwargs)
    fig.subplots_adjust(left=0., right=1., top=1., bottom=0.)
    ax.set_axis_off()
    ax.set_xlim(auto=False)
    ax.set_ylim(auto=False)
    return fig, ax

def add_background(ax, n=200):
    # Generate points
    n_sqrt = int(np.sqrt(n))
    def random_edges(direction=0):
        Xi = np.random.rand(2*n_sqrt, 2)
        Xi[:,direction] = np.round(Xi[:,direction])
        return Xi
    X = np.r_[np.random.rand(n, 2),               # scatter
              random_edges(0),                    # left & right
              random_edges(1),                    # top & bottom
              np.indices((2,2)).T.reshape(-1,2)]  # corners

    # Delaunay triangulation
    tri = Delaunay(X)

    # Create polygons
    triangles = X[tri.simplices.copy()]
    polygons = [Polygon(xy) for xy in triangles]

    # Create polygons with gradient
    # polygons = []
    # for xy in triangles:
    #     x_mid = np.mean(xy, axis=0)
    #     for factor in np.logspace(-2., 1., 20):
    #         xyi = xy + factor*(x_mid-xy)
    #         polygons.append(Polygon(xyi))
    # colors = np.repeat(colors, 20)
    p = PatchCollection(polygons, alpha=0.4, match_original=False)

    # Color polygon based on distance to origin
    colors = np.sqrt(np.sum(np.square(triangles.mean(axis=1)), axis=1))
    p.set_clim(-0.3, 1.3)
    p.set_array(colors)

    # Draw on ax
    ax.triplot(X[:,0], X[:,1], tri.simplices.copy(), alpha=0.5, c="w", lw=0.5)
    ax.add_collection(p)
    return ax

def save_svg(fig, fname, attributes={}, **kwargs):
    import xml.etree.ElementTree as ET
    from io import BytesIO
    if kwargs.pop("format", "svg") != "svg":
        raise ValueError("figure save format must be svg")
    if not fname.endswith(".svg"):
        fname = fname + ".svg"

    bio = BytesIO()
    fig.savefig(bio, format="svg", **kwargs)
    element = ET.XML(bio.getvalue())
    for key, value in attributes.items():
        element.set(key, value)
    return ET.ElementTree(element).write(fname)

if __name__=="__main__":
    np.random.seed(50)
    
    svg_attr = {"preserveAspectRatio": "none"}
    fig, ax = subplots_axis_off(figsize=(16,9))
    add_background(ax, n=100)
    save_svg(fig, "../static/images/background-large.svg",
             attributes=svg_attr)
    # fig.savefig("../static/images/background-small.png", dpi=400)

    fig, ax = subplots_axis_off(figsize=(9/2,16/2))
    add_background(ax, n=25)
    save_svg(fig, "../static/images/background-small.svg",
             attributes=svg_attr)
    # fig.savefig("../static/images/background-large.png", dpi=200)