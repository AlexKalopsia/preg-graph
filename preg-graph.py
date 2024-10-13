import argparse

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from scipy.interpolate import PchipInterpolator

from styles import styles


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default='data.csv', required=False, 
        help='The CSV file to import data from')
    parser.add_argument('-o', '--output', type=str, default='graph.png', required=False, 
        help='The PNG filename to export')
    parser.add_argument('--columns', type=int, default=3, required=False, 
        help='The amount of columns the exported figure should have')
    parser.add_argument('--style', type=str, choices=styles.keys(), default='default', 
        help='The style to use')
    parser.add_argument('--dpi', type=int, default=300, required=False, 
        help='The output resolution of the exported figure')

    args = parser.parse_args()
    if args.columns <= 0:
        parser.error('--columns must be greater than 0')

    # Pull data, and clean NaN
    data_raw = pd.read_csv(args.input)
    data = data_raw.replace([np.inf, -np.inf], np.nan).fillna(0)

    # Skip first column (Week)
    categories = list(data.columns[1:])
    x_header = 'Week'

    STYLE_PARAMS = styles[args.style].params
    COLUMNS = args.columns

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

    # Settings
    TITLE = 'Pregnancy Overview'
    X_LABEL = 'Week'
    SPLINE_RES = 300
    WEEK_MIN = 4
    WEEK_MAX = 42
    WEEK_BIRTH = 38 # set to None if birth hasn't occurred yet
    INTENSITY_MIN = 0
    INTENSITY_MAX = 5
    WEIGHT_MIN = 55
    WEIGHT_MAX = 75

    # Styling
    SUBPLOTS_HSPACING = 0.7
    SUBPLOTS_WSPACING = 0.4

    TEXT_COLOR = STYLE_PARAMS.text_color
    LINE = STYLE_PARAMS.line
    DOT = STYLE_PARAMS.dot
    GRID_ALPHA = STYLE_PARAMS.grid_alpha
    TRIMESTER_SEPARATOR_ALPHA = STYLE_PARAMS.trimesters_separator_alpha
    TRIMESTER_COLORS = STYLE_PARAMS.trimesters_color
    BIRTH_SEPARATOR = STYLE_PARAMS.birth_separator
    POST_BIRTH_COLOR = STYLE_PARAMS.post_birth_color
    BACKGROUND_COLOR = STYLE_PARAMS.background_color
    GRAPH_BACKGROUND_COLOR = STYLE_PARAMS.graph_background_color

    mpl.rcParams['text.color'] = TEXT_COLOR

    fig.suptitle(TITLE, fontweight='bold', fontsize=24)
    fig.patch.set_facecolor(BACKGROUND_COLOR)

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
        ax.set_title(cat_name, fontweight='bold', color=TEXT_COLOR, pad=16)
        x_data = data[x_header]
        y_data = data[cat_name]

        # Setup spline
        spl = PchipInterpolator(x_data, y_data)
        x_new = np.linspace(x_data.min(), x_data.max(), num=SPLINE_RES)
        y_smooth = spl(x_new)

        # Set graph parameters
        regular_ticks = np.arange(WEEK_MIN, WEEK_MAX + 1, 4)
        all_ticks = np.unique(np.append(regular_ticks, WEEK_BIRTH)) if WEEK_BIRTH is not None else regular_ticks

        ax.set_xticks(all_ticks)
        ax.set_yticks(np.arange(MIN_YTICK, MAX_YTICK, INCR_YTICK))
        ax.set_xticklabels(ax.get_xticks(), color=TEXT_COLOR)
        ax.set_yticklabels(ax.get_yticks(), color=TEXT_COLOR)
        ax.set_xlabel(X_LABEL, labelpad=8, color=TEXT_COLOR)
        ax.set_ylabel(Y_LABEL, labelpad=16, color=TEXT_COLOR)
        ax.set_xlim(left=X_MIN, right=X_MAX)
        ax.set_ylim(bottom=Y_MIN, top=Y_MAX)
        ax.grid(True, alpha=GRID_ALPHA)

        # Styling
        ax.set_facecolor(GRAPH_BACKGROUND_COLOR)
        for spine in ax.spines.values():
            spine.set_edgecolor(TEXT_COLOR)
        ax.tick_params(axis='x', colors=TEXT_COLOR)
        ax.tick_params(axis='y', colors=TEXT_COLOR)
        # Trimester background styles
        trimester_first = Rectangle((0, ax.get_ylim()[0]), 12, 
                      ax.get_ylim()[1] - ax.get_ylim()[0], 
                      color=TRIMESTER_COLORS[0].hex, alpha=TRIMESTER_COLORS[0].alpha)
        ax.add_patch(trimester_first)
        trimester_second = Rectangle((12, ax.get_ylim()[0]), 16, 
                      ax.get_ylim()[1] - ax.get_ylim()[0], 
                      color=TRIMESTER_COLORS[1].hex, alpha=TRIMESTER_COLORS[1].alpha)
        ax.add_patch(trimester_second)
        fill_limit = ax.get_xlim()[1] - 28 if WEEK_BIRTH is None else WEEK_BIRTH - 28
        trimester_third = Rectangle((28, ax.get_ylim()[0]), fill_limit, 
                      ax.get_ylim()[1] - ax.get_ylim()[0], 
                      color=TRIMESTER_COLORS[2].hex, alpha=TRIMESTER_COLORS[2].alpha)
        ax.add_patch(trimester_third)

        # Make trimester separators darker for each graph
        vertical_lines = ax.get_xgridlines()
        # Len check to prevent our of bound issues
        if len(vertical_lines) > 2:
            vertical_lines[2].set(alpha=TRIMESTER_SEPARATOR_ALPHA)
        if len(vertical_lines) > 6:
            vertical_lines[6].set(alpha=TRIMESTER_SEPARATOR_ALPHA)

        if WEEK_BIRTH is not None:
            # We cover the grid line relative to the tick
            ax.axvline(x=WEEK_BIRTH, color=GRAPH_BACKGROUND_COLOR, 
                linestyle='solid', linewidth=1,
                alpha=1.0)
            ax.axvline(x=WEEK_BIRTH, color=POST_BIRTH_COLOR.hex, 
                linestyle='solid', linewidth=1,
                alpha=POST_BIRTH_COLOR.alpha)
            fill = Rectangle((WEEK_BIRTH, ax.get_ylim()[0]), 
                  ax.get_xlim()[1] - WEEK_BIRTH, 
                  ax.get_ylim()[1] - ax.get_ylim()[0], 
                  color=POST_BIRTH_COLOR.hex, alpha=POST_BIRTH_COLOR.alpha) 
            ax.add_patch(fill)
            # We draw the pregnancy birth separatror, if we have one
            ax.axvline(x=WEEK_BIRTH, color=BIRTH_SEPARATOR.color.hex, 
                linestyle=BIRTH_SEPARATOR.style.value, linewidth=BIRTH_SEPARATOR.width,
                alpha=BIRTH_SEPARATOR.color.alpha, label='Birth')

        # Draw spline
        ax.plot(x_new, y_smooth, label=cat_name, linestyle=LINE.style.value, 
            linewidth=LINE.width, color=LINE.color.hex, alpha=LINE.color.alpha)
        # Draw dots
        dot_sizes = [DOT.size] * len(x_data)
        if WEEK_BIRTH is not None:
            for i, x in enumerate(x_data):
                if x == WEEK_BIRTH:
                    dot_sizes[i] = DOT.size * 7

        ax.scatter(x_data, y_data, s=dot_sizes, color=DOT.color.hex, alpha=DOT.color.alpha, zorder=5)

        # Draw a special dot at birth
        if WEEK_BIRTH is not None:
            closest_index = (np.abs(x_data - WEEK_BIRTH)).idxmin()  
            y_target = y_data.iloc[closest_index]
            ax.scatter(WEEK_BIRTH, y_target, s=DOT.size, color=LINE.color.hex, alpha=1.0, zorder=6)

    # Delete leftover empty axes
    for i in range(len(categories), len(axes_flat)):
        fig.delaxes(axes_flat[i])       

    # Watermark
    fig.text(0.98, 0.02, 'made with ' + r'$ \bf{preg\text{-}graph}$', 
        ha='right', va='bottom')

    # Export figure
    plt.subplots_adjust(hspace=SUBPLOTS_HSPACING, wspace=SUBPLOTS_WSPACING)
    plt.savefig(args.output, dpi=args.dpi)
    #plt.show()

if __name__ == '__main__':
    main()