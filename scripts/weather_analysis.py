import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import seaborn as sns
import matplotlib

class WeatherAnalysis:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the analyzer with a weather DataFrame.

        :param df: The DataFrame containing weather data.
        """
        self.df = df

    def generate_intervals_labels(self, attribute, split, gap):
        """
        Generate intervals and labels for a given attribute.

        :param attribute: The attribute to generate intervals for.
        :param split: The number of intervals to split the data into.
        :param gap: The gap between each interval.
        :return: A tuple of intervals and labels.
        """
        var_min = min(self.df[attribute])
        intervals = [int(var_min)]
        labels = []
        for i in range(1, split+1):
            lower_limit = int(var_min+((i-1)*gap))
            if i==split:
                upper_limit = int(max(self.df[attribute]))
            else:
                upper_limit = int(var_min + (i*gap))
            intervals.append(upper_limit)
            label_var = '({} to {})'.format(lower_limit, upper_limit)
            labels.append(label_var)
        return intervals, labels

    def feature_bin_plot(self, dataframe, attribute, clrs, intervals, labels, fig_size, font_size, y_lim, adjust, title):
        """
        Create a bar plot for a given attribute.

        :param dataframe: The DataFrame to plot.
        :param attribute: The attribute to plot.
        :param clrs: The color scheme to use.
        :param intervals: The intervals to plot.
        :param labels: The labels for the intervals.
        :param fig_size: The size of the figure.
        :param font_size: The font size to use.
        :param y_lim: The limits for the y-axis.
        :param adjust: The adjustment for the text labels.
        :param title: The title of the plot.
        """
        new_df = dataframe.copy()
        xlabel = f'Different {attribute} Grouped Value'
        new_df[xlabel] = pd.cut(new_df[attribute], bins=intervals, labels=labels, include_lowest=True)

        temp_df = pd.DataFrame(new_df[xlabel].value_counts().reset_index())
        temp_df.columns = ['Bins', 'Cases']

        count, max_index = 0, 0
        cases_list = list(temp_df['Cases'])
        for i in cases_list:
            if i == max(temp_df['Cases']):
                max_index = count
                count += 1

        total = len(new_df[xlabel])
        plt.figure(figsize=fig_size)
        cmap = cm.get_cmap(clrs, len(intervals))
        clrs = [mcolors.rgb2hex(cmap(i)) for i in range(len(intervals))]

        ax = sns.barplot(y=temp_df['Cases'], x=temp_df['Bins'], palette=clrs)
        for i in ax.patches:
            ax.text(i.get_x() + adjust[0], i.get_height() + adjust[-1],
                    f'{int(i.get_height()):,d}\nCases\n({round(100 * i.get_height() / total, 2)}%)',
                    fontsize=font_size, color='black')

        plt.title(title, size=15, color='grey')
        plt.ylim(y_lim)

        for i in ['bottom', 'top', 'left', 'right']:
            ax.spines[i].set_color('white')
            ax.spines[i].set_linewidth(1)

        ax.set_xlabel(f'\n{xlabel}\n', fontsize=15, color='grey')
        ax.set_ylabel('\nAccident Cases\n', fontsize=15, color='grey')

        ax.grid(color='#b2b2b2', linewidth=1, alpha=.3)
        ax.tick_params(axis='both', which='major', labelsize=12)
        MA = mpatches.Patch(color=clrs[max_index], label=f'{attribute} Range with\n no. of Road Accidents')
        ax.legend(handles=[MA], prop={'size': 10.5}, loc='best', borderpad=1, edgecolor='white')

        plt.show()

    def different_temperature_range(self, df):
        temp_intervals, temp_labels = self.generate_intervals_labels('Temperature(F)', 9, 30)
        self.feature_bin_plot(df, 'Temperature(F)', 'gist_ncar', temp_intervals, temp_labels,
                  (12, 6), 14, (-20000, 4000000), [0.01, 10000], '\nPercentage of different Temperature range\n')
        
    def humidity_intervals(self, df):
        humidity_intervals, humidity_labels = self.generate_intervals_labels('Humidity(%)', 10, 10)
        self.feature_bin_plot(df, 'Humidity(%)','magma', humidity_intervals, humidity_labels, 
                              (12, 6), 14, (-20000, 1200000), [0.01, 10000], '\nPercentage of different Humidity range\n')

    def pressure_range(self, df):
        pressure_intervals, pressure_labels = self.generate_intervals_labels('Pressure(in)', 6, 10)
        self.feature_bin_plot(df, 'Pressure(in)', 'Paired', pressure_intervals, pressure_labels, 
                              (12, 6), 14, (-20000, 5400000), [0.01, 10000], '\nPercentage of Pressure range\n')

    def visibility_range(self, df):
        visibility_intervals, visibility_labels = self.generate_intervals_labels('Visibility(mi)', 12, 1)
        self.feature_bin_plot(df, 'Visibility(mi)', 'Paired', visibility_intervals, visibility_labels, 
                              (12, 6), 14, (-20000, 6100000), [0.01, 300], '\nPercentage of Visibility range\n')
        


def weather_condition(df):
    weather_condition_df = pd.DataFrame(df.Weather_Condition.value_counts().head(10)).reset_index().rename(columns={'Cases':'Weather_Condition', 'count':'Cases'})

    fig, ax = plt.subplots(figsize = (10,8), dpi = 80)

    cmap = cm.get_cmap('rainbow_r', 10)   
    clrs = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]

    ax=sns.barplot(x=weather_condition_df['Cases'], y=weather_condition_df['Weather_Condition'], palette='rainbow_r')

    total = df.shape[0]
    for p in ax.patches:
        plt.text(p.get_width()+40000, p.get_y()+0.4,
                '{:.2f}%'.format(p.get_width()*100/total),ha='center', va='center', fontsize=15, color='black', weight='bold')

    plt.title('\nRoad Accident Percentage \nfor different Weather Condition in US (2016-2020)\n', size=20, color='grey')
    plt.xlabel('\nAccident Cases\n', fontsize=15, color='grey')
    plt.ylabel('\nWeather_Condition\n', fontsize=15, color='grey')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=12)
    plt.xlim(0, 2500000)

    for i in ['top', 'left', 'right']:
        side = ax.spines[i]
        side.set_visible(False)

    ax.set_axisbelow(True)
    ax.spines['bottom'].set_bounds(0, 600000)
    ax.grid(color='#b2d6c7', linewidth=1, axis='y', alpha=.3)

    MA = mpatches.Patch(color=clrs[0], label='Weather_Condition with Maximum\n no. of Road Accidents')
    ax.legend(handles=[MA], prop={'size': 10.5}, loc='best', borderpad=1, 
            labelcolor=[clrs[0]], edgecolor='white');