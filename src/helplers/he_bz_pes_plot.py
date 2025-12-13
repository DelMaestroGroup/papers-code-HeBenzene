import matplotlib.pyplot as plt
import numpy as np


def set_pub_style(font_size=12):

    plt.rc("font", size=10)
    plt.rc("xtick", labelsize=font_size)
    plt.rc("ytick", labelsize=font_size)
    plt.rc("axes", labelsize=font_size)
    plt.rc("legend", fontsize=font_size)


def plot_curves_on_axis(
    ax, x_data, curves_config, xlabel, ylabel, legend_loc="upper right"
):

    for curve in curves_config:
        ax.plot(
            x_data,
            curve["y_data"],
            label=curve.get("label"),
            linewidth=curve.get("linewidth", 1.0),
            linestyle=curve.get("linestyle", "-"),
            marker=curve.get("marker", "o"),
            markersize=curve.get("markersize", 2),
            color=curve.get("color", None),
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc=legend_loc)
    ax.grid(True, alpha=0.3, linestyle="--")


def get_benzene_coords_array():
    """
    Defines the orientation of the benzene molecule
    """
    z_val = 0
    coord = []
    benzene = f"""
    C    -1.2073830   -0.6970829    {z_val}
    C    -1.2073830    0.6970829    {z_val}
    C     0.0000000    1.3941659    {z_val}
    C     1.2073830    0.6970829    {z_val}
    C     1.2073830   -0.6970829    {z_val}
    C     0.0000000   -1.3941659    {z_val}
    H    -2.1490090   -1.2407309    {z_val}
    H    -2.1490090    1.2407309    {z_val}
    H     0.0000000    2.4814619    {z_val}
    H     2.1490090    1.2407309    {z_val}
    H     2.1490090   -1.2407309    {z_val}
    H     0.0000000   -2.4814619    {z_val}"""
    for line in benzene.split("\n"):
        if line:
            atom, x, y, z = line.split()
            if atom == "C":
                coord.append([0, float(x), float(y), float(z)])
            elif atom == "H":
                coord.append([1, float(x), float(y), float(z)])

    return coord


def plot_benzene(ax):
    c = get_benzene_coords_array()
    for i in range(6):
        ax.plot([c[i][1], c[i + 6][1]], [c[i][2], c[i + 6][2]], ".-", color="lavender")
    for j in range(6):
        ax.plot(
            [c[j][1], c[(j + 1) % 6][1]],
            [c[j][2], c[(j + 1) % 6][2]],
            ".-",
            color="black",
        )
    return True


def plot_inset_benzene(ax, inset_position, *q_args):

    inax = ax.inset_axes(inset_position, projection="3d")

    plot_benzene(inax)
    val = [5, 0, 0]
    labels = [r"$x$", r"$y$", r"$z$"]

    for v in range(3):
        xv = [val[v - 0], -val[v - 0]]
        yv = [val[v - 1], -val[v - 1]]
        zv = [val[v - 2], -val[v - 2]]
        inax.plot(xv, yv, zv, "k-", linewidth=1)
        inax.text(
            val[v - 0] + 0.2,
            val[v - 1],
            val[v - 2],
            labels[v],
            color="black",
            fontsize=6,
        )

    inax._axis3don = False
    inax.set_facecolor("none")
    inax.quiver(*q_args, color="blue", length=0.5, arrow_length_ratio=0.3)

    inax.set_xlim(np.array([-2, 5]))
    inax.set_ylim(np.array([-2, 5]))
    inax.set_zlim(np.array([-2, 5]))

    inax.set_xticks([])
    inax.set_yticks([])
    inax.set_zticks([])
