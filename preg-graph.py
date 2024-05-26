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

symptoms = ['Nausea', 'Fatigue', 'Diarrhea', 'Sore Breasts', 'Breathlessness', 'Smell Sensitivity', 'Stomach Pain', 'Bad Taste in Mouth', 'Migraine', 'Heartburn', 'Knee Pain', 'Hip Pain', 'Sweating']

MOSAIC_COLUMNS = 2
num_arrays = -(-len(symptoms) // MOSAIC_COLUMNS)
split_symptoms = [symptoms[i*MOSAIC_COLUMNS:(i+1)*MOSAIC_COLUMNS] for i in range(num_arrays)]
last_array_length = len(split_symptoms[-1])
desired_length = MOSAIC_COLUMNS
if last_array_length < desired_length:
    split_symptoms[-1] += [None] * (desired_length - last_array_length)
print(split_symptoms)

fig, ax_dict = plt.subplot_mosaic(split_symptoms)
fig.suptitle('Symptoms')


for i in range(len(symptoms)):
    if (symptoms[i] != None):
        ax = ax_dict[symptoms[i]]
        ax.set_title(symptoms[i])
        x_data = data['Week']
        y_data = data[symptoms[i]]
        #print(y_data)
        SPLINE_RES = 500
        spl = PchipInterpolator(x_data, y_data)
        x_new = np.linspace(x_data.min(), x_data.max(), num=SPLINE_RES)
        y_smooth = spl(x_new)
        # Draw
        ax.fill_between(x_new, 5, where = x_new < 13, facecolor='#f0f0f0', alpha=0.5)
        ax.fill_between(x_new, 5, where = (x_new >= 13) & (x_new < 28), facecolor='#f0f0f0', alpha=0.3)
        ax.fill_between(x_new, 5, where = x_new > 28, facecolor='#f0f0f0', alpha=0.5)
        ax.set_xticks(np.arange(data[x_header].min(), data[x_header].max() + 1, 4))
        ax.set_xlabel('Week')
        ax.set_ylabel('Intensity')
        ax.set_xlim(left=WEEK_MIN-1, right=WEEK_MAX)
        ax.plot(x_new, y_smooth, label=symptoms[i], linestyle='--', color='orange')
        ax.scatter(x_data, y_data, s=6, color='blue', zorder=5)

plt.savefig('test.png')
#plt.show()