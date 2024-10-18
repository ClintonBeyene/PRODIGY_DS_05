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
from Levenshtein import *
from itertools import product
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from scipy.spatial.distance import pdist, squareform
from shapely.geometry import Point, Polygon

class StreetAccidentAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.street_df = pd.DataFrame(df['Street'].value_counts()).reset_index().rename(columns={'Street': 'Street No.', 'count': 'Cases'})

    def street_analysis(self, df):
        # create a dataframe of Street and their corresponding accident
        street_df = pd.DataFrame(df['Street'].value_counts()).reset_index().rename(columns={'Street': 'Street No.', 'count': 'Cases'})

        top_ten_streets_df = pd.DataFrame(street_df.head(10))

        FIGSIZE = (12, 6)
        DPI = 80
        NUM_COLORS = 10

        fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
                
        cmap = cm.get_cmap('gnuplot2', NUM_COLORS)   
        clrs = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]

        ax = sns.barplot(y=top_ten_streets_df['Cases'], x=top_ten_streets_df['Street No.'], palette='gnuplot2')
        ax1 = ax.twinx()
        sns.lineplot(data=top_ten_streets_df, marker='o', x='Street No.', y='Cases', color='white', alpha=.8)

        total_streets = df.shape[0]
        for i in ax.patches:
            ax.text(i.get_x()+0.5, i.get_height()-3000, 
                    '{:,d}'.format(int(i.get_height())), fontsize=12.5, weight='bold',
                        color='white')
            
        ax.set_ylim(-1000, 79000)
        ax1.set_ylim(-1000, 40000)
        plt.title('Top 10 Accident Prone Streets in US (2016-2023)', fontsize=20, color='grey')

        ax1.axes.yaxis.set_visible(False)
        ax.set_xlabel('Street No.', fontsize=15, color='grey')
        ax.set_ylabel('Accident Cases', fontsize=15, color='grey')

        for i in ['top', 'right']:
            side1 = ax.spines[i]
            side1.set_visible(False)
            side2 = ax1.spines[i]
            side2.set_visible(False)

            
        ax.set_axisbelow(True)
        ax.grid(color='#b2d7c7', linewidth=1, axis='y', alpha=.3)

        ax.spines['bottom'].set_bounds(0.005, 9)
        ax.spines['left'].set_bounds(0, 30000)
        ax1.spines['bottom'].set_bounds(0.005, 9)
        ax1.spines['left'].set_bounds(0, 30000)
        ax.tick_params(axis='both', which='major', labelsize=12)

        MA = mpatches.Patch(color=clrs[1], label='Street with Maximum no. of Road Accidents')
        MI = mpatches.Patch(color=clrs[-2], label='Street with Minimum no. of Road Accidents')
        ax.legend(handles=[MA, MI], prop={'size': 10.5}, loc='best', borderpad=1, 
                labelcolor=[clrs[1], 'grey'], edgecolor='white')
        
        plt.show()

    def street_cases_percentage(self, val: int, operator: str) -> str:
        """
        Calculate the number and percentage of streets with the given condition.

        :param val: The value to compare with the 'Cases' column.
        :param operator: The operator to use for comparison. Supported operators are '<', '>', and '='.
        :return: A string containing the result.
        """

        # Validate the operator
        if operator not in ['<', '>', '=']:
            raise ValueError("Invalid operator. Supported operators are '<', '>', and '='.")

        # Validate the value
        if not isinstance(val, int):
            raise TypeError("Value must be an integer.")

        # Perform the comparison
        if operator == '<':
            mask = self.street_df['Cases'] < val
        elif operator == '>':
            mask = self.street_df['Cases'] > val
        else:  # operator == '='
            mask = self.street_df['Cases'] == val

        # Calculate the number and percentage of streets
        num_streets = mask.sum()
        percentage = round((num_streets / len(self.street_df)) * 100, 2)

        # Return the result as a string
        return f"{num_streets} streets ({percentage:.2f}%) have {val} accident cases."

    def main(self):
        # Print the result:
        total_streets = len(self.street_df)
        print(f"In this Dataset, we have the records of total {total_streets} Streets.")

        print(self.street_cases_percentage(1, '='))
        print(self.street_cases_percentage(100, '<'))
        print(self.street_cases_percentage(1000, '<'))
        print(self.street_cases_percentage(1000, '>'))
        print(self.street_cases_percentage(5000, '>'))
        print(self.street_cases_percentage(10000, '>'))