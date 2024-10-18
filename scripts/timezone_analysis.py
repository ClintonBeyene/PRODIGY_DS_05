# import all necesary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from matplotlib import cm
import matplotlib.colors as mcolors
import seaborn as sns
import calendar
import plotly as pt
from plotly import graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from pylab import *
import matplotlib.patheffects as PathEffects
from shapely.geometry import Point
from geopy.geocoders import Nominatim
import time
from retrying import retry

import descartes
import geopandas as gpd
from Levenshtein import distance
from itertools import product
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from scipy.spatial.distance import pdist, squareform
from shapely.geometry import Point, Polygon

def timezone_analysis(df):
    timezone_df = pd.DataFrame(df['Timezone'].value_counts()).reset_index().rename(columns={'index':'Timezone', 'count':'Cases'})
    fig, ax = plt.subplots(figsize=(10,6), dpi=80)

    cmap = cm.get_cmap('spring', 4)   
    clrs = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]

    ax=sns.barplot(y=timezone_df['Cases'], x=timezone_df['Timezone'], palette='spring')

    total = df.shape[0]
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2, i.get_height() + 5000, \
                '{}%'.format(round(i.get_height()*100/total)), fontsize=15, weight='bold',
                    color='black', ha='center')

    ax.set_ylim(-20000, 3900000)
    ax.set_title('\nPercentage of Accident Cases for \ndifferent Timezone in US (2016-2023)\n', size=20, color='grey')
    ax.set_ylabel('\nAccident Cases\n', fontsize=15, color='grey')
    ax.set_xlabel('\nTimezones\n', fontsize=15, color='grey')
    ax.tick_params(axis='x', labelsize=13)
    ax.tick_params(axis='y', labelsize=12)

    for i in ['top', 'right']:
        side = ax.spines[i]
        side.set_visible(False)
        
    ax.set_axisbelow(True)
    ax.grid(color='#b2d6c7', linewidth=1, axis='y', alpha=.3)
    ax.spines['bottom'].set_bounds(0.005, 3)
    ax.spines['left'].set_bounds(0, 700000)

    MA = mpatches.Patch(color=clrs[0], label='Timezone with Maximum\n no. of Road Accidents')
    MI = mpatches.Patch(color=clrs[3], label='Timezone with Minimum\n no. of Road Accidents')
    ax.legend(handles=[MA, MI], prop={'size': 10.5}, loc='best', borderpad=1, 
            labelcolor=[clrs[0], 'grey'], edgecolor='white')