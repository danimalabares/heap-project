#!/usr/bin/env python3
"""Draw an exact real affine slice of quadratic Cremona linkage.

Run from the repository root: python3 scripts/draw_cremona_linkage.py
Dependencies: numpy, matplotlib, and TeX Live's Latin Modern fonts.

The target lines U+V-2W=0 and 2U-3V+W=0 meet at [1:1:1].
Under [x:y:z] -> [yz:xz:xy], their pullbacks are smooth conics.
They meet at the three coordinate points and [1:1:1], all reduced.
Both panels use the affine chart where the sum of coordinates is 1.
The plotted coordinates are (y,z), respectively (V,W).
These are real slices of complex projective planes, not whole planes.
"""

from pathlib import Path
import subprocess

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reading-assets" / "linkage-cremona.png"
for style in ("regular", "italic", "bold"):
    font_path = subprocess.check_output(
        ["kpsewhich", f"lmroman10-{style}.otf"], text=True
    ).strip()
    font_manager.fontManager.addfont(font_path)
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman"],
    "mathtext.fontset": "cm",
    "font.size": 15,
})

TEAL = "#278378"
PURPLE = "#7654a3"
ORANGE = "#cf5b16"
INK = "#263444"
grid = np.linspace(-0.22, 1.2, 1000)
u, v = np.meshgrid(grid, grid)
x = 1-u-v
conic_1 = u*v+x*v-2*x*u
conic_2 = 2*u*v-3*x*v+x*u
line_1 = 1-3*v
line_2 = 2-5*u-v

fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.9),
                         facecolor="white")
for ax in axes:
    ax.set_aspect("equal")
    ax.set(xlim=(-0.22, 1.2), ylim=(-0.22, 1.2))
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#d9dee3")

ax = axes[0]
ax.set_title("Source: two conics", pad=13)
ax.contour(u, v, conic_1, levels=[0], colors=[TEAL],
           linewidths=2.5)
ax.contour(u, v, conic_2, levels=[0], colors=[PURPLE],
           linewidths=2.5)
ax.scatter([0, 1, 0], [0, 0, 1], s=80, color=INK,
           edgecolor="white", linewidth=1.2, zorder=5)
ax.scatter([1/3], [1/3], s=105, color=ORANGE,
           edgecolor="white", linewidth=1.5, zorder=6)
for px, py, label, offset in [
    (0, 0, "$[1:0:0]$", (6, -24)),
    (1, 0, "$[0:1:0]$", (-68, -24)),
    (0, 1, "$[0:0:1]$", (6, 9)),
    (1/3, 1/3, "$p$", (9, 10)),
]:
    ax.annotate(label, (px, py), xytext=offset,
                textcoords="offset points",
                color=ORANGE if label == "$p$" else INK)
ax.legend(handles=[
    Line2D([], [], color=TEAL, lw=2.5, label="$D_1$"),
    Line2D([], [], color=PURPLE, lw=2.5, label="$D_2$"),
], loc="upper right", frameon=False, fontsize=13)

ax = axes[1]
ax.set_title("Target: two lines", pad=13)
ax.contour(u, v, line_1, levels=[0], colors=[TEAL],
           linewidths=2.5)
ax.contour(u, v, line_2, levels=[0], colors=[PURPLE],
           linewidths=2.5)
ax.scatter([1/3], [1/3], s=105, color=ORANGE,
           edgecolor="white", linewidth=1.5, zorder=6)
ax.annotate("$q$", (1/3, 1/3), xytext=(10, 10),
            textcoords="offset points", color=ORANGE)
ax.text(0.96, 0.37, r"$\ell_1$", color=TEAL)
ax.text(0.22, 1.03, r"$\ell_2$", color=PURPLE)

fig.text(0.5, 0.57, r"$\varphi$", ha="center", fontsize=20)
axes[0].annotate("", xy=(0.535, 0.53), xytext=(0.465, 0.53),
                 xycoords=fig.transFigure,
                 arrowprops={"arrowstyle": "->", "lw": 1.6,
                             "color": INK})
legend = [
    Line2D([], [], marker="o", color="none", markerfacecolor=INK,
           markersize=8, label="Three base points: map undefined"),
    Line2D([], [], marker="o", color="none", markerfacecolor=ORANGE,
           markersize=8, label="Residual point $p$ maps to $q$"),
]
fig.legend(handles=legend, loc="lower center", ncol=2,
           frameon=False, fontsize=12,
           bbox_to_anchor=(0.5, 0.015), columnspacing=2)
fig.subplots_adjust(left=0.03, right=0.97, top=0.88,
                    bottom=0.15, wspace=0.28)
OUT.parent.mkdir(exist_ok=True)
fig.savefig(OUT, dpi=220, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Wrote {OUT.relative_to(ROOT)}")
