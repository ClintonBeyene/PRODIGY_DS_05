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

class StateAnalyzer:
    def __init__(self, df):
        self.df = df
        self.us_states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'}
        
    def create_state_df(self):
        state_df = self.df['State'].value_counts().reset_index().rename(columns={'index':'State', 'count':'Cases'})
        state_df['State'] = state_df['State'].apply(self.us_states.get)
        return state_df
    
    def top_10_states(self, state_df):
        top_ten_states = state_df.nlargest(10, 'Cases')
        return top_ten_states
    
    def least_10_states(self, state_df):
        least_ten_states = state_df.nsmallest(10, 'Cases')
        return least_ten_states
    
    
    def plot_top_states(self, df, top_ten_states):
        
        fig, ax = plt.subplots(figsize = (12,6), dpi = 80)

        cmap = cm.get_cmap('winter', 10)   
        clrs = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]

        ax=sns.barplot(y=top_ten_states['Cases'].head(10), x=top_ten_states['State'].head(10), palette='winter')
        ax1 = ax.twinx()
        sns.lineplot(data = top_ten_states[:10], marker='o', x='State', y='Cases', color = 'white', alpha = .8)


        total = df.shape[0]
        for i in ax.patches:
            ax.text(i.get_x()-0.2, i.get_height()+10000, \
                    ' {:,d}\n  ({}%) '.format(int(i.get_height()), round(100*i.get_height()/total, 1)), fontsize=15,
                        color='black')


        ax.set(ylim =(-10000, 1800000))
        ax1.set(ylim =(-100000, 1700000))

        plt.title('\nTop 10 States with most no. of \nAccident cases in US (2016-2023)\n', size=20, color='grey')
        ax1.axes.yaxis.set_visible(False)
        ax.set_xlabel('\nStates\n', fontsize=15, color='grey')
        ax.set_ylabel('\nAccident Cases\n', fontsize=15, color='grey')

        for i in ['top','right']:
            side1 = ax.spines[i]
            side1.set_visible(False)
            side2 = ax1.spines[i]
            side2.set_visible(False)
            
        ax.set_axisbelow(True)
        ax.grid(color='#b2d6c7', linewidth=1, axis='y', alpha=.3)

        ax.spines['bottom'].set_bounds(0.005, 9)
        ax.spines['left'].set_bounds(0, 600000)
        ax1.spines['bottom'].set_bounds(0.005, 9)
        ax1.spines['left'].set_bounds(0, 600000)
        ax.tick_params(axis='y', which='major', labelsize=10.6)
        ax.tick_params(axis='x', which='major', labelsize=10.6, rotation=10)

        MA = mpatches.Patch(color=clrs[0], label='State with Maximum\n no. of Road Accidents')
        ax.legend(handles=[MA], prop={'size': 10.5}, loc='best', borderpad=1, 
                labelcolor=clrs[0], edgecolor='white'); 

    def plot_least_states(self, df, least_ten_states):
        fig, ax = plt.subplots(figsize = (12,6), dpi = 80)

        cmap = cm.get_cmap('cool', 10)   
        clrs = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]

        ax=sns.barplot(y=least_ten_states['Cases'].tail(10), x=least_ten_states['State'].tail(10), palette='cool')
        ax1 = ax.twinx()
        sns.lineplot(data = least_ten_states[-10:], marker='o', x='State', y='Cases', color = 'white', alpha = .8)

        total = df.shape[0]
        for i in ax.patches:
            ax.text(i.get_x()-0.1, i.get_height()+100, \
                    '  {:,d}\n({}%) '.format(int(i.get_height()), round(100*i.get_height()/total, 2)), fontsize=15,
                        color='black')

        ax.set(ylim =(-50, 15000))
        ax1.set(ylim =(-50, 6000))

        plt.title('\nTop 10 States with least no. of \nAccident cases in US (2016-2023)\n', size=20, color='grey')
        ax1.axes.yaxis.set_visible(False)
        ax.set_xlabel('\nStates\n', fontsize=15, color='grey')
        ax.set_ylabel('\nAccident Cases\n', fontsize=15, color='grey')

        for i in ['top', 'right']:
            side = ax.spines[i]
            side.set_visible(False)
            side1 = ax1.spines[i]
            side1.set_visible(False)
            
            
        ax.set_axisbelow(True)
        ax.grid(color='#b2d6c7', linewidth=1, axis='y', alpha=.3)

        ax.spines['bottom'].set_bounds(0.005, 9)
        ax.spines['left'].set_bounds(0, 5000)
        ax1.spines['bottom'].set_bounds(0.005, 9)
        ax1.spines['left'].set_bounds(0, 5000)
        ax.tick_params(axis='y', which='major', labelsize=11)
        ax.tick_params(axis='x', which='major', labelsize=11, rotation=15)

        MI = mpatches.Patch(color=clrs[-1], label='State with Minimum\n no. of Road Accidents')
        ax.legend(handles=[MI], prop={'size': 10.5}, loc='best', borderpad=1, 
                labelcolor=clrs[-1], edgecolor='white');