import matplotlib.pyplot as plt

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def mplu_realcircle(ax, x, y, x_radius):
    from matplotlib.patches import Ellipse
    from matplotlib.patheffects import withStroke

    # calculate asymmetry of x and y axes:
    x0, y0 = ax.transAxes.transform((0,0)) # lower left in pixels
    x1, y1 = ax.transAxes.transform((1,1)) # upper right in pixes
    dx = x1 - x0
    dy = y1 - y0
    xlim0, xlim1 = ax.get_xlim()
    ylim0, ylim1 = ax.get_ylim()
    dx_data = xlim1 - xlim0
    dy_data = ylim1 - ylim0
    width = x_radius * 2
    height = width * (dy_data * dx) / (dx_data * dy)

    circle = Ellipse((x, y), width, height, clip_on=False, zorder=10, linewidth=1,
                    edgecolor='black', facecolor=(0, 0, 0, .0125),
                    path_effects=[withStroke(linewidth=5, foreground='w')])
    ax.add_artist(circle)


# - - - - - - - - - - - - - - - - - - - - - - - - - -
def mplu_text(ax, x, y, text):
    ax.text(x, y, text,
            ha='center', va='center', color='black')




