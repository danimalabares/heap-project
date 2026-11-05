#!/usr/bin/env python3
"""Draw an exact real affine slice of a projective linkage example.

The smooth cubic is F=x(x*x+y*y-w*w)+z(w*w+z*z).
Its section z=0 is the line x=0 and the conic x*x+y*y=w*w.
These are original explanatory figures, not copies of talk slides.
Run from the repository root: python3 scripts/draw_linkage_example.py
Dependencies: numpy and matplotlib.

Smoothness over C follows directly from the four partial derivatives:
3x^2+y^2-w^2, 2xy, w^2+3z^2, 2w(z-x). If x=0 they force
w=z=y=0. Otherwise y=0; w=0 forces z=x=0, while z=x would
give both w^2=3x^2 and w^2=-3x^2. There is no projective solution.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reading-assets"
OUT.mkdir(exist_ok=True)
BLUE = "#1765a8"
ORANGE = "#d05a19"
GREY = "#788491"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12})

# In w=1, the real root of z^3+z=-x(x^2+y^2-1) is unique.
grid = np.linspace(-1.5, 1.5, 151)
x, y = np.meshgrid(grid, grid)
rhs = -x * (x*x + y*y - 1)
z = 2 / np.sqrt(3) * np.sinh(
    np.arcsinh(3*np.sqrt(3)*rhs/2) / 3
)
assert np.max(np.abs(z**3 + z - rhs)) < 1e-12
theta = np.linspace(0, 2*np.pi, 501)
circle_x, circle_y = np.cos(theta), np.sin(theta)
assert np.max(np.abs(circle_x**2 + circle_y**2 - 1)) < 1e-12

fig = plt.figure(figsize=(10, 5.7), facecolor="white")
ax = fig.add_subplot(111, projection="3d", computed_zorder=False)
ax.plot_surface(
    x, y, z, color="#75a796", alpha=0.37,
    rstride=4, cstride=4, linewidth=0.18,
    edgecolor="#5b8879", zorder=1,
)
corners = [(-1.5, -1.5, 0), (1.5, -1.5, 0),
           (1.5, 1.5, 0), (-1.5, 1.5, 0)]
plane = Poly3DCollection(
    [corners], facecolor="#c9c3e2", edgecolor="#9289b0",
    alpha=0.23, linewidth=1, zorder=2,
)
ax.add_collection3d(plane)
ax.plot(np.zeros_like(grid), grid, np.zeros_like(grid),
        color=BLUE, lw=3.5, zorder=5)
ax.plot(circle_x, circle_y, np.zeros_like(theta),
        color=ORANGE, lw=3.5, zorder=6)
ax.scatter([0, 0], [-1, 1], [0, 0], color="#253548",
           s=33, depthshade=False, zorder=7)
ax.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), zlim=(-1.8, 1.8))
ax.set_xlabel("x", labelpad=0)
ax.set_ylabel("y", labelpad=0)
ax.text2D(.96, .55, "z", transform=ax.transAxes)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.view_init(elev=25, azim=-52)
ax.set_box_aspect((1, 1, 0.73))
ax.grid(False)
ax.set_title("A plane cuts a cubic surface in a line and a conic", pad=4)
legend = [
    Line2D([0], [0], color="#75a796", lw=7, alpha=.6,
           label="Cubic surface S"),
    Line2D([0], [0], color="#c9c3e2", lw=7,
           label="Cutting plane z = 0"),
    Line2D([0], [0], color=BLUE, lw=3, label="Known line L"),
    Line2D([0], [0], color=ORANGE, lw=3, label="Residual conic C"),
]
fig.legend(handles=legend, loc="lower center", ncol=2,
           frameon=False, bbox_to_anchor=(.5, .0))
fig.subplots_adjust(left=.02, right=.98, top=.90, bottom=.12)
fig.savefig(OUT / "linkage-cubic-plane.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close(fig)

fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.25), facecolor="white")
titles = ["1. Whole plane section", "2. Identify the known line",
          "3. Take the residual conic"]
for i, ax in enumerate(axes):
    ax.set_aspect("equal")
    ax.set(xlim=(-1.45, 1.45), ylim=(-1.45, 1.45))
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#d8dce1")
    ax.axhline(0, color="#e5e8eb", lw=.8, zorder=0)
    ax.axvline(0, color="#e5e8eb", lw=.8, zorder=0)
    ax.set_title(titles[i], fontsize=11, pad=10)
    ax.plot(circle_x, circle_y, color=ORANGE,
            lw=3, alpha=.15 if i == 1 else 1)
    ax.plot([0, 0], [-1.35, 1.35], color=BLUE,
            lw=3, alpha=.2 if i == 2 else 1,
            linestyle="--" if i == 2 else "-")
    if i != 1:
        ax.scatter([0, 0], [-1, 1], s=30, color="#253548", zorder=5)
    ax.text(.72, .78, "C", color=ORANGE, fontsize=14,
            alpha=.3 if i == 1 else 1)
    ax.text(.1, 1.15, "L", color=BLUE, fontsize=14,
            alpha=.3 if i == 2 else 1)
fig.text(.5, .02, "Residuality keeps the two meeting points (black dots).",
         ha="center", color="#394858", fontsize=11)
fig.subplots_adjust(left=.02, right=.98, top=.85, bottom=.13, wspace=.15)
fig.savefig(OUT / "linkage-residual-conic.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Wrote two exact linkage illustrations to reading-assets/.")
