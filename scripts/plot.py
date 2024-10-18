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

import geoplot
from geopy.geocoders import Nominatim

import warnings
warnings.filterwarnings('ignore')

def top_10cities(df):
    # convert the Start_Time & End_Time Variable into Datetime Feature
    df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='ISO8601')
    df['End_Time'] = pd.to_datetime(df['End_Time'], format='ISO8601')

    city_df = df['City'].value_counts().reset_index().rename(columns={'index':'City', 'count':'Cases'})

    top_10_cities = pd.DataFrame(city_df.head(10)) 

    # Ensure 'top_10_cities' DataFrame is sorted
    top_10_cities = top_10_cities.sort_values(by='Cases', ascending=False)

    # Calculate total cases
    total_cases_country = city_df['Cases'].sum()

    # Create a bar chart with Plotly Express
    fig = px.bar(top_10_cities, x='City', y='Cases', 
                text=top_10_cities['Cases'].apply(lambda x: f"{(x / total_cases_country) * 100:.2f}%"),
                color='City', 
                color_discrete_sequence=px.colors.sequential.Viridis)

    # Calculate the percentage of top 10 cities' cases from the total country cases
    top_10_cases = top_10_cities['Cases'].sum()
    percentage_top_10 = (top_10_cases / total_cases_country) * 100

    # Update layout
    fig.update_layout(
        title='\nTop 10 Cities in US with most Road Accident Cases (2016 - 2023)\n',
        xaxis_title='\nCities\n',
        yaxis_title='\nAccident Cases\n',
        font=dict(color='grey', size=15),
        xaxis=dict(tickangle=10, tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
        plot_bgcolor='white',
        annotations=[
            dict(
                x=0.5,
                y=-0.25,
                xref='paper',
                yref='paper',
                text=f"Top 10 Cities account for {percentage_top_10:.2f}% of total cases",
                showarrow=False,
                font=dict(size=14, color="grey"),
                align="center"
            )
        ]
    )

    # Add hover template to show percentages
    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",  # Positioning the text inside the bars
        insidetextanchor="end",  # Centering the text
        textangle=0,  # Ensuring the text is horizontal
        hovertemplate="<b>%{x}</b><br>%{y} cases<br>%{text}"
    )

    fig.show()


def calculate_kpis(city_df):
    """
    Calculate KPIs related to accident cases in a city.
    
    Parameters:
    city_df (pandas.DataFrame): DataFrame containing city-level accident data.
    
    Returns:
    tuple: Weekly cases and average daily cases.
    """
    # Get the highest number of cases reported in the city
    highest_cases = city_df.Cases[0]
    
    # Calculate weekly cases
    weekly_cases = round(highest_cases / 8)
    
    # Calculate average daily cases
    average_daily_cases = round(highest_cases / (8 * 365))
    
    return weekly_cases, average_daily_cases


def top_10_accident_prone_city(city_df):
    # Load US states shapefile
    states = gpd.read_file("../data/maps/us-states.json")

    # Load top 10 cities from city_df
    top_ten_city_list = list(city_df.City.head(10))

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def lat(city):
        address = city
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(address)
        return location.latitude

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def lng(city):
        address = city
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(address)
        return location.longitude

    # Generate lat/lng for top 10 cities
    top_ten_city_lat_dict = {city: lat(city) for city in top_ten_city_list}
    top_ten_city_lng_dict = {city: lng(city) for city in top_ten_city_list}

    # Filter top 10 cities from original DataFrame
    top_10_cities_df = city_df[city_df['City'].isin(top_ten_city_list)]

    # Add new columns with latitude and longitude for each city
    top_10_cities_df['New_Start_Lat'] = top_10_cities_df['City'].map(top_ten_city_lat_dict)
    top_10_cities_df['New_Start_Lng'] = top_10_cities_df['City'].map(top_ten_city_lng_dict)

    # Create a GeoDataFrame
    geometry_cities = [Point(xy) for xy in zip(top_10_cities_df['New_Start_Lng'], top_10_cities_df['New_Start_Lat'])]
    geo_df_cities = gpd.GeoDataFrame(top_10_cities_df, geometry=geometry_cities)

    # Plot configuration
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_xlim([-125, -65])
    ax.set_ylim([22, 55])

    # Plot states boundaries and names
    states.boundary.plot(ax=ax, color='grey')
    for idx, row in states.iterrows():
        plt.annotate(text=row['name'], xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                    horizontalalignment='center', fontsize=10, color='black')

    # Custom colors and marker sizes
    colors = ['#e6194B','#f58231','#ffe119','#bfef45','#3cb44b',
            '#aaffc3','#42d4f4','#4363d8','#911eb4','#f032e6']
    markersizes = [50 + (i * 20) for i in range(10)][::-1]

    # Plot top 10 cities
    for i in range(10):
        geo_df_cities[geo_df_cities['City'] == top_ten_city_list[i]].plot(
            ax=ax, 
            markersize=markersizes[i], 
            color=colors[i], 
            marker='o', 
            label=top_ten_city_list[i], 
            alpha=0.7
        )

    plt.legend(prop={'size': 13, 'family': 'Arial'}, loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5),
            edgecolor='white', title="Cities", title_fontsize=15)

    # Plot aesthetics
    for spine in ['bottom', 'top', 'left', 'right']:
        ax.spines[spine].set_visible(False)

    plt.tick_params(top=False, bottom=False, left=False, right=False,
                    labelleft=False, labelbottom=False)

    plt.title('\nVisualization of Top 10 Accident-Prone Cities in US (2016-2020)', 
            size=20, color='grey', fontname='Arial')

    plt.show()


class CityAccidentAnalyzer:
    def __init__(self, city_df: pd.DataFrame):
        """
        Initialize the analyzer with a city DataFrame.

        :param city_df: The DataFrame containing city data.
        """
        self.city_df = city_df

    def city_cases_percentage(self, val: int, operator: str) -> (int, float):
        """
        Calculate the number and percentage of cities with cases matching the given condition.

        :param val: The value to compare with the 'Cases' column.
        :param operator: The comparison operator. Supported operators are '<', '>', and '='.
        :return: The number of cities and the percentage.
        """
        # Validate the operator
        if operator not in ['<', '>', '=']:
            raise ValueError("Supported operators are '<', '>', and '='.")

        # Create a mask based on the operator
        if operator == '<':
            mask = self.city_df['Cases'] < val
        elif operator == '>':
            mask = self.city_df['Cases'] > val
        else:  # operator == '='
            mask = self.city_df['Cases'] == val

        # Calculate the number of cities and percentage
        num_cities = mask.sum()
        percentage = round((num_cities / len(self.city_df)) * 100, 2)

        return num_cities, percentage

    def print_results(self) -> None:
        """
        Print the results of the analysis.
        """
        total_cities = len(self.city_df)
        print(f"In this Dataset, we have the records of total {total_cities} Cities.")

        num_cities, percentage = self.city_cases_percentage(1, '=')
        print(f"7. {percentage:.2f}% ({num_cities} Cities) cities in US, have only {1} accident record in past 8 years.")

        num_cities, percentage = self.city_cases_percentage(100, '<')
        print(f"8. Around {percentage:.2f}% ({num_cities} Cities) of all cities in US, have less than {100} total no. of road accidents.")

        num_cities, percentage = self.city_cases_percentage(1000, '<')
        print(f"9. {percentage:.2f}% ({num_cities} Cities) cities in US, have the road accident records (2016-2023), less than {1000}.")

        num_cities, percentage = self.city_cases_percentage(1000, '>')
        print(f"10. There are {num_cities} Cities ({percentage:.2f}%) in US, which have more than {1000} total no. of road accidents in past 8 years.")

        num_cities, percentage = self.city_cases_percentage(5000, '>')
        print(f"11. {num_cities} Cities ({percentage:.2f}%) in US, have more than {5000} road accident records.")

        num_cities, percentage = self.city_cases_percentage(10000, '>')
        print(f"12. Only {num_cities} Cities ({percentage:.2f}%) in US, have more than {10000} road accident records.")

