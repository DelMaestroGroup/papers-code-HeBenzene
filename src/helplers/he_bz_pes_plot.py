import matplotlib.pyplot as plt


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
