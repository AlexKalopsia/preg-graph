from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
from scipy.interpolate import PchipInterpolator


@dataclass
class Style:
    background_color: str
    graph_background_color: str
    text_color: str
    line_style: str
    line_color: str
    line_width: float
    dot_color: str
    dot_size: float
    trimesters_color: List[Tuple[str, float]] 
    trimesters_separator_alpha: float
    grid_alpha: float

class FigureStyle(Enum):
    DEFAUL = Style(
        background_color='#fff',
        graph_background_color='#fff',
        text_color='#000',
        line_style='--',
        line_color='#ffa500',
        line_width=2,
        dot_color='blue',
        dot_size=8,
        trimesters_color=[['#fff', 1.0], ['#fff', 1.0], ['#fff', 1.0]],
        trimesters_separator_alpha=0.65,
        grid_alpha=0.2
    )
    DARK = Style(
        background_color='#0d1117',
        graph_background_color='#010409',
        text_color='#e8eff4',
        line_style='-',
        line_color='#b37a09',
        line_width=2,
        dot_color='#ffa500',
        dot_size=10,
        trimesters_color=[['#010409', 1.0], ['#010409', 1.0], ['#010409', 1.0]],
        trimesters_separator_alpha=0.65,
        grid_alpha=0.05
    )

    @property
    def name(self):
        return self._name

    @property
    def style(self):
        return self._style

# Pull data, and clean NaN
data_raw = pd.read_csv('data.csv')
data = data_raw.replace([np.inf, -np.inf], np.nan).fillna(0)

x_header = 'Week'
categories = ['Anxiety', 'Fatigue', 'Breathlessness', 'Smell Sensitivity', 'Nausea',
'Stomach Pain', 'Diarrhea', 'Incontinence', 'Bad Taste in Mouth', 'Migraine',
'Heartburn', 'Sore Breasts', 'Knee Pain', 'Hip Pain', 'Hands Swelling/Pain',
'Sweating', 'Weight']

CURRENT_STYLE = FigureStyle.DEFAUL

COLUMNS = 3
# Based on the amount of columns, split data in separate arrays per raw
num_arrays = -(-len(categories) // COLUMNS)
RAWS = num_arrays
split_categories = [categories[i*COLUMNS:(i+1)*COLUMNS] for i in range(num_arrays)]

# Build grid
for i in range(len(split_categories)):
    while len(split_categories[i]) < COLUMNS:
        split_categories[i].append(None)

fig, axes = plt.subplots(num_arrays, COLUMNS, figsize=(10 * COLUMNS, 4 * RAWS))
axes_flat = axes.flatten()

TITLE = 'Pregnancy Overview'
X_LABEL = 'Week'

# Styling
SPLINE_RES = 300
SUBPLOTS_HSPACING = 0.7
SUBPLOTS_WSPACING = 0.4
TEXT_COLOR = CURRENT_STYLE.value.text_color
LINE_COLOR = CURRENT_STYLE.value.line_color
LINE_STYLE = CURRENT_STYLE.value.line_style
LINE_WIDTH = CURRENT_STYLE.value.line_width
DOTS_COLOR = CURRENT_STYLE.value.dot_color
DOTS_SIZE = CURRENT_STYLE.value.dot_size
TRIMESTER_STYLES = CURRENT_STYLE.value.trimesters_color
TRIMESTER_SEPARATOR_ALPHA = CURRENT_STYLE.value.trimesters_separator_alpha
#TRIMESTER_STYLES = [['#f788a6', 0.2], ['#f5e6bc', 0.2], ['#cce7fc', 0.1]]    # Colored
#TRIMESTER_STYLES = [['#f0f0f0', 0.8], ['#f0f0f0', 0.4], ['#f0f0f0', 0.1]]    # Grayscale
GRID_ALPHA = CURRENT_STYLE.value.grid_alpha
BACKGROUND_COLOR = CURRENT_STYLE.value.background_color
GRAPH_BACKGROUND_COLOR = CURRENT_STYLE.value.graph_background_color

mpl.rcParams['text.color'] = TEXT_COLOR
mpl.rcParams['axes.labelcolor'] = TEXT_COLOR
mpl.rcParams['xtick.color'] = TEXT_COLOR
mpl.rcParams['ytick.color'] = TEXT_COLOR
mpl.rcParams['axes.titlecolor'] = TEXT_COLOR

fig.suptitle(TITLE, fontweight='bold', fontsize=24)
fig.patch.set_facecolor(BACKGROUND_COLOR)

WEEK_MIN = 4
WEEK_MAX = 42
INTENSITY_MIN = 0
INTENSITY_MAX = 5
WEIGHT_MIN = 55
WEIGHT_MAX = 75

# Do a graph (ax) per category
for i, cat_name in enumerate(categories):

    # Set correct labels and parameters
    Y_LABEL = 'Kg' if cat_name == 'Weight' else 'Intensity'
    MIN_YTICK = WEIGHT_MIN if cat_name == 'Weight' else INTENSITY_MIN
    MAX_YTICK = WEIGHT_MAX + 1 if cat_name == 'Weight' else INTENSITY_MAX + 0.5
    INCR_YTICK = 5 if cat_name == 'Weight' else 1
    X_MIN = WEEK_MIN - 2
    X_MAX = WEEK_MAX
    Y_MIN = WEIGHT_MIN - 2 if cat_name == 'Weight' else INTENSITY_MIN - 0.5
    Y_MAX = WEIGHT_MAX + 2 if cat_name == 'Weight' else INTENSITY_MAX + 0.5

    # Setup graph data
    ax = axes_flat[i]
    ax.set_title(cat_name, fontweight='bold', pad=16)

    x_data = data[x_header]
    y_data = data[cat_name]

    # Setup spline
    spl = PchipInterpolator(x_data, y_data)
    x_new = np.linspace(x_data.min(), x_data.max(), num=SPLINE_RES)
    y_smooth = spl(x_new)

    # Set graph parameters
    ax.set_xticks(np.arange(x_data.min(), x_data.max() + 1, 4))
    ax.set_yticks(np.arange(MIN_YTICK, MAX_YTICK, INCR_YTICK))
    ax.set_xticklabels(ax.get_xticks(), color=TEXT_COLOR)
    ax.set_yticklabels(ax.get_yticks(), color=TEXT_COLOR)
    ax.set_xlabel(X_LABEL, labelpad=8, color=TEXT_COLOR)
    ax.set_ylabel(Y_LABEL, labelpad=16, color=TEXT_COLOR)
    ax.set_xlim(left=X_MIN, right=X_MAX)
    ax.set_ylim(bottom=Y_MIN, top=Y_MAX)
    ax.grid(True, alpha=GRID_ALPHA)

    for spine in ax.spines.values():
        spine.set_edgecolor(TEXT_COLOR)
        #spine.set_linewidth(TEXT_COLOR)
        #spine.set_linestyle(TEXT_COLOR)

    ax.tick_params(axis='x', colors=TEXT_COLOR)  # Set x-axis tick label color
    ax.tick_params(axis='y', colors=TEXT_COLOR)

    ax.set_facecolor(GRAPH_BACKGROUND_COLOR)

    # Trimester background styles
    ax.fill_between(x_new, 5, where = x_new < 12, facecolor=TRIMESTER_STYLES[0][0],
                    alpha=TRIMESTER_STYLES[0][1])
    ax.fill_between(x_new, 5, where = (x_new >= 12) & (x_new < 28), 
                    facecolor=TRIMESTER_STYLES[1][0], alpha=TRIMESTER_STYLES[1][1])
    ax.fill_between(x_new, 5, where = x_new >= 28, facecolor=TRIMESTER_STYLES[2][0],
                    alpha=TRIMESTER_STYLES[2][1])

    # Draw spline
    ax.plot(x_new, y_smooth, label=cat_name, linestyle=LINE_STYLE, linewidth=LINE_WIDTH,
            color=LINE_COLOR)
    # Draw dots
    ax.scatter(x_data, y_data, s=DOTS_SIZE, color=DOTS_COLOR, zorder=5)



# Delete leftover empty axes
for i in range(len(categories), len(axes_flat)):
    fig.delaxes(axes_flat[i])

# Make trimester separators darker for each graph
for ax in axes_flat:
    if ax is not None:
        vertical_lines = ax.get_xgridlines()
        # Len check to prevent our of bound issues
        if len(vertical_lines) > 2:
            vertical_lines[2].set(alpha=TRIMESTER_SEPARATOR_ALPHA)
        if len(vertical_lines) > 6:
            vertical_lines[6].set(alpha=TRIMESTER_SEPARATOR_ALPHA)

bold_font = FontProperties(weight='bold')
fig.text(0.98, 0.02, 'made with ' + r'$ \bf{preg\text{-}graph}$', ha='right', va='bottom')

# Export figure
plt.subplots_adjust(hspace=SUBPLOTS_HSPACING, wspace=SUBPLOTS_WSPACING)
plt.savefig('graph.png', dpi=300)
#plt.show()