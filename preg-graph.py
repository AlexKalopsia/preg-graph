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
y_header = 'Nausea'

symptoms = ['Nausea', 'Fatigue', 'Diarrhea', 'Sore Breasts', 'Breathlessness', 'Smell Sensitivity', 'Stomach Pain', 'Bad Taste in Mouth', 'Migraine', 'Heartburn', 'Knee Pain', 'Hip Pain', 'Sweating']

x_data = data[x_header]
y_data = data[y_header]

print(data.head())

SPLINE_RES = 500
spl = PchipInterpolator(data[x_header], data[y_header]) # 3 = cubic
x_new = np.linspace(data[x_header].min(), data[x_header].max(), num=SPLINE_RES)
y_smooth = spl(x_new)

#spline = make_interp_spline(x_data,y_data)
plt.fill_between(x_new, 5, where = x_new < 13, facecolor='#f0f0f0', alpha=0.5)
plt.fill_between(x_new, 5, where = (x_new >= 13) & (x_new < 28), facecolor='#f0f0f0', alpha=0.3)
plt.fill_between(x_new, 5, where = x_new > 28, facecolor='#f0f0f0', alpha=0.5)

plt.plot(x_new, y_smooth, label=y_header, linestyle='--', color='orange')
plt.scatter(x_data, y_data, s=12, color='blue', zorder=5)
plt.xlim(left=WEEK_MIN-1, right=WEEK_MAX)
plt.xticks(np.arange(data[x_header].min(), data[x_header].max() + 1, 4))
#plt.plot(x_data, y_data)
plt.xlabel('Week')
plt.ylabel('Intensity')
#plt.subplot_mosaic
plt.title(y_header)
#plt.legend()
plt.show()


#df = pd.DataFrame({'x_values': range(WEEK_MIN,WEEK_MAX), 'y_values': np.random.randn(WEEK_MAX-WEEK_MIN)})
#plt.plot('x_values', 'y_values', data=df, color='skyblue')
#plt.show()
#plt.plot( 'x_values', 'y_values', data=df, color='skyblue', alpha=0.3, linewidth=3)
#plt.show()

#values=np.cumsum(np.random.randn(1000,1))
#plt.plot(values)
#plt.show()