import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from matplotlib.patches import FancyArrowPatch, ArrowStyle, ConnectionPatch
from matplotlib.patheffects import withStroke

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def convert_x_len_in_equivalent_y_len(ax, x):
    x0, y0 = ax.transAxes.transform((0,0)) # lower left in pixels
    x1, y1 = ax.transAxes.transform((1,1)) # upper right in pixes
    dx = x1 - x0
    dy = y1 - y0
    xlim0, xlim1 = ax.get_xlim()
    ylim0, ylim1 = ax.get_ylim()
    dx_data = xlim1 - xlim0
    dy_data = ylim1 - ylim0
    return x * (dy_data * dx) / (dx_data * dy)

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def mplu_realcircle(ax, x, y, x_radius):

    # calculate asymmetry of x and y axes:
    y_radius = convert_x_len_in_equivalent_y_len(ax, x_radius)

    circle = Ellipse((x, y), x_radius*2, y_radius*2, clip_on=False, zorder=10, linewidth=1,
                    edgecolor='black', facecolor=(0, 0, 0, .0125),
                    path_effects=[withStroke(linewidth=5, foreground='w')])
    ax.add_artist(circle)


# - - - - - - - - - - - - - - - - - - - - - - - - - -
def mplu_text(ax, x, y, text, color='black'):
    ax.text(x, y, text,
            ha='center', va='center', color=color)

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def mplu_realsquare(ax, x, y, x_side, **kwargs):
    _color=kwargs.get('color', 'black')
    y_side = convert_x_len_in_equivalent_y_len(ax, x_side)
    rect = Rectangle((x, y), x_side, y_side)
    rect.set_color(_color)
    ax.add_artist(rect)

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def mplu_arrow(ax, x0, y0, x1, y1, **kwargs):
    _color=kwargs.get('color', 'black')
    _scale=kwargs.get('scale', 25)
    arrow = FancyArrowPatch((x0, y0), (x1, y1),
                            arrowstyle=ArrowStyle('Simple', head_width=1, head_length=1),
                            mutation_scale=_scale)
    arrow.set_color(_color)
    ax.add_artist(arrow)

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def mplu_line(ax, x0, y0, x1, y1, **kwargs):
    _color=kwargs.get('color', 'black')
    _lwidth=kwargs.get('width', 4)
    line = ConnectionPatch((x0,y0), (x1,y1), 'data', axesA=ax)
    line.set_color(_color)
    line.set_linewidth(_lwidth)
    ax.add_artist(line)

