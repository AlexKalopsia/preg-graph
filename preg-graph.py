import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline, PchipInterpolator

WEEK_MIN = 4
WEEK_MAX = 44

INTENSITY_MIN = 0
INTENSITY_MAX = 5

data_raw = pd.read_csv('graph.csv')
# Clean data from NaN
data = data_raw.replace([np.inf, -np.inf], np.nan).fillna(0)

x_header = 'Week'
symptoms = ['Nausea', 'Fatigue', 'Sore Breasts', 'Breathlessness', 'Smell Sensitivity', 'Stomach Pain', 'Diarrhea', 'Bad Taste in Mouth', 'Migraine', 'Heartburn', 'Knee Pain', 'Hip Pain', 'Sweating', 'Weight']

MOSAIC_COLUMNS = 4
num_arrays = -(-len(symptoms) // MOSAIC_COLUMNS)
split_symptoms = [symptoms[i*MOSAIC_COLUMNS:(i+1)*MOSAIC_COLUMNS] for i in range(num_arrays)]

for i in range(len(split_symptoms)):
    while len(split_symptoms[i]) < MOSAIC_COLUMNS:
        split_symptoms[i].append(None)

fig, axes = plt.subplots(num_arrays, MOSAIC_COLUMNS, figsize=(10 * MOSAIC_COLUMNS, 4 * num_arrays))


fig.suptitle('Pregnancy Overview',  fontweight='bold')

#colors = [['#f788a6', 0.2], ['#f5e6bc', 0.2], ['#cce7fc', 0.1]]    # Colored
#colors = [['#f0f0f0', 0.8], ['#f0f0f0', 0.4], ['#f0f0f0', 0.1]]    # Grayscale
colors = [['#fff', 1.0], ['#fff', 1.0], ['#fff', 1.0]]              # White

SUBPLOTS_HSPACING = 0.7
SUBPLOTS_WSPACING = 0.4

X_LABEL = 'Week'


LINE_COLOR = 'orange'
LINE_STYLE = '--'
LINE_WIDTH = 2
DOTS_COLOR = 'blue'
DOTS_SIZE = 8

axes_flat = axes.flatten()

for i, symptom in enumerate(symptoms):
    ax = axes_flat[i]
    ax.set_title(symptom, fontweight='bold', pad=16)
    x_data = data[x_header]
    y_data = data[symptom]

    SPLINE_RES = 500
    Y_LABEL = 'Kg' if symptom == 'Weight' else 'Intensity'
    MIN_YTICK = 55 if symptom == 'Weight' else 0
    MAX_YTICK = 76 if symptom == 'Weight' else 6
    INCR_YTICK = 5 if symptom == 'Weight' else 1
    Y_MIN = 52 if symptom == 'Weight' else -1
    Y_MAX = 77 if symptom == 'Weight' else 6

    spl = PchipInterpolator(x_data, y_data)
    x_new = np.linspace(x_data.min(), x_data.max(), num=SPLINE_RES)
    y_smooth = spl(x_new)
    # Draw
    ax.grid(True, alpha=0.2)
    ax.fill_between(x_new, 5, where = x_new < 12, facecolor=colors[0][0], alpha=colors[0][1])
    ax.fill_between(x_new, 5, where = (x_new >= 12) & (x_new < 28), facecolor=colors[1][0], alpha=colors[1][1])
    ax.fill_between(x_new, 5, where = x_new >= 28, facecolor=colors[2][0], alpha=colors[2][1])
    ax.set_xticks(np.arange(x_data.min(), x_data.max() + 1, 4))
    ax.set_yticks(np.arange(MIN_YTICK, MAX_YTICK, INCR_YTICK))
    ax.set_xlabel(X_LABEL, labelpad=8)
    ax.set_ylabel(Y_LABEL, labelpad=16)
    ax.set_xlim(left=WEEK_MIN-1, right=WEEK_MAX)
    ax.set_ylim(bottom=Y_MIN, top=Y_MAX)
    ax.plot(x_new, y_smooth, label=symptom, linestyle=LINE_STYLE, linewidth=LINE_WIDTH, color=LINE_COLOR)
    ax.scatter(x_data, y_data, s=DOTS_SIZE, color=DOTS_COLOR, zorder=5)

for i in range(len(symptoms), len(axes_flat)):
    fig.delaxes(axes_flat[i])

# Make trimester separators darker
for ax in axes_flat:
    if ax is not None:
        vertical_lines = ax.get_xgridlines()
        if len(vertical_lines) > 2:  # Check if there's a second vertical line
            #vertical_lines[2].set_linewidth(2)
            vertical_lines[2].set(alpha=0.6)  # Set the thickness to 2 points
        if len(vertical_lines) > 6:  # Check if there's a second vertical line
            #vertical_lines[6].set_linewidth(2)
            vertical_lines[6].set(alpha=0.6)  # Set the thickness to 2 points

plt.subplots_adjust(hspace=SUBPLOTS_HSPACING, wspace=SUBPLOTS_WSPACING) 
plt.savefig('graph.png', dpi=300)

#plt.show()