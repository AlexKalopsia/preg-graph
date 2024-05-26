import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline, PchipInterpolator



# Pull data, and clean NaN
data_raw = pd.read_csv('graph.csv')
data = data_raw.replace([np.inf, -np.inf], np.nan).fillna(0)

x_header = 'Week'
categories = ['Nausea', 'Fatigue', 'Sore Breasts', 'Breathlessness', 'Smell Sensitivity', 'Stomach Pain', 'Diarrhea', 'Bad Taste in Mouth', 'Migraine', 'Heartburn', 'Knee Pain', 'Hip Pain', 'Sweating', 'Weight']

COLUMNS = 4
num_arrays = -(-len(categories) // COLUMNS)
split_categories = [categories[i*COLUMNS:(i+1)*COLUMNS] for i in range(num_arrays)]
RAWS = num_arrays

# Build grid
for i in range(len(split_categories)):
    while len(split_categories[i]) < COLUMNS:
        split_categories[i].append(None)

fig, axes = plt.subplots(num_arrays, COLUMNS, figsize=(10 * COLUMNS, 4 * RAWS))
axes_flat = axes.flatten()

TITLE = 'Pregnancy Overview'
X_LABEL = 'Week'

fig.suptitle(TITLE, fontweight='bold')

# Styling
SPLINE_RES = 300
SUBPLOTS_HSPACING = 0.7
SUBPLOTS_WSPACING = 0.4
LINE_COLOR = 'orange'
LINE_STYLE = '--'
LINE_WIDTH = 2
DOTS_COLOR = 'blue'
DOTS_SIZE = 8
COLORS = [['#fff', 1.0], ['#fff', 1.0], ['#fff', 1.0]]              # White
#COLORS = [['#f788a6', 0.2], ['#f5e6bc', 0.2], ['#cce7fc', 0.1]]    # Colored
#COLORS = [['#f0f0f0', 0.8], ['#f0f0f0', 0.4], ['#f0f0f0', 0.1]]    # Grayscale

WEEK_MIN = 4
WEEK_MAX = 44
INTENSITY_MIN = 0
INTENSITY_MAX = 5
WEIGHT_MIN = 55
WEIGHT_MAX = 75

for i, name in enumerate(categories):
    ax = axes_flat[i]
    ax.set_title(name, fontweight='bold', pad=16)
    x_data = data[x_header]
    y_data = data[name]

    Y_LABEL = 'Kg' if name == 'Weight' else 'Intensity'
    MIN_YTICK = WEIGHT_MIN if name == 'Weight' else INTENSITY_MIN
    MAX_YTICK = WEIGHT_MAX + 1 if name == 'Weight' else INTENSITY_MAX + 1
    INCR_YTICK = 5 if name == 'Weight' else 1
    Y_MIN = WEIGHT_MIN - 2 if name == 'Weight' else INTENSITY_MIN - 1
    Y_MAX = WEIGHT_MAX + 2 if name == 'Weight' else INTENSITY_MAX + 1

    spl = PchipInterpolator(x_data, y_data)
    x_new = np.linspace(x_data.min(), x_data.max(), num=SPLINE_RES)
    y_smooth = spl(x_new)
    ax.grid(True, alpha=0.2)
    ax.fill_between(x_new, 5, where = x_new < 12, facecolor=COLORS[0][0], alpha=COLORS[0][1])
    ax.fill_between(x_new, 5, where = (x_new >= 12) & (x_new < 28), facecolor=COLORS[1][0], alpha=COLORS[1][1])
    ax.fill_between(x_new, 5, where = x_new >= 28, facecolor=COLORS[2][0], alpha=COLORS[2][1])
    ax.set_xticks(np.arange(x_data.min(), x_data.max() + 1, 4))
    ax.set_yticks(np.arange(MIN_YTICK, MAX_YTICK, INCR_YTICK))
    ax.set_xlabel(X_LABEL, labelpad=8)
    ax.set_ylabel(Y_LABEL, labelpad=16)
    ax.set_xlim(left=WEEK_MIN-1, right=WEEK_MAX)
    ax.set_ylim(bottom=Y_MIN, top=Y_MAX)
    ax.plot(x_new, y_smooth, label=name, linestyle=LINE_STYLE, linewidth=LINE_WIDTH, color=LINE_COLOR)
    ax.scatter(x_data, y_data, s=DOTS_SIZE, color=DOTS_COLOR, zorder=5)

# Deleate leftover empty axes
for i in range(len(categories), len(axes_flat)):
    fig.delaxes(axes_flat[i])

# Make trimester separators darker
for ax in axes_flat:
    if ax is not None:
        vertical_lines = ax.get_xgridlines()
        if len(vertical_lines) > 2:
            vertical_lines[2].set(alpha=0.6)
        if len(vertical_lines) > 6:
            vertical_lines[6].set(alpha=0.6)

# Export figure
plt.subplots_adjust(hspace=SUBPLOTS_HSPACING, wspace=SUBPLOTS_WSPACING) 
plt.savefig('graph.png', dpi=300)
#plt.show()