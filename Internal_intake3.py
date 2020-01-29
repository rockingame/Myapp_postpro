import glob
from typing import Any, Union
from pandas import Series, DataFrame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np
import os

if not os.path.exists('temporary_results'):
    os.makedirs('temporary_results')
todelete_files = glob.glob('temporary_results/*.txt')
for f in todelete_files:
    os.remove(f)
scenario = glob.glob('*.csv')
for file in scenario:
    df = pd.read_csv(file)
# define temperature range
    df = df.dropna(subset=['Mean Temperature In C']).copy()
    max_temp = math.ceil(max(df['Mean Temperature In C']))
    min_temp = math.floor(min(df['Mean Temperature In C']))
    n_temp = (max_temp - min_temp) * 2
    tldf = pd.DataFrame(np.linspace(min_temp, max_temp, n_temp+1))
# Count temperature in range
    tls = pd.Series(tldf[0])
    counttest = df.groupby(
        pd.cut(df['Mean Temperature In C'], tls, right=False)).count()
    mtic_segment = counttest.iloc[:, 0:1].copy()
    mtic_segment.reset_index(inplace=True)
    mtic_segment.columns = ['Inlet Temperature', 'Number of IT Equipment']
    # Calculate percentage
    # total numbers of the IT servers
    n_servers: Union[Union[Series, DataFrame], Any] = df['Location ID'].count()
    n_servers = int(n_servers)
    # calculate percentage
    mtic_segment.iloc[:, 1] = mtic_segment.iloc[:, 1] / n_servers
    # Generate data frame
    temp_range_dictionary = {
        '[14.0, 14.5)': '14≤T<14.5 \u00b0C', '[14.5, 15.0)': '14.5≤T<15 \u00b0C',
        '[15.0, 15.5)': '15≤T<15.5 \u00b0C', '[15.5, 16.0)': '15.5≤T<16 \u00b0C',
        '[16.0, 16.5)': '16≤T<16.5 \u00b0C', '[16.5, 17.0)': '16.5≤T<17 \u00b0C',
        '[17.0, 17.5)': '17≤T<17.5 \u00b0C', '[17.5, 18.0)': '17.5≤T<18 \u00b0C',
        '[18.0, 18.5)': '18≤T<18.5 \u00b0C', '[18.5, 19.0)': '18.5≤T<19 \u00b0C',
        '[19.0, 19.5)': '19≤T<19.5 \u00b0C', '[19.5, 20.0)': '19.5≤T<20 \u00b0C',
        '[20.0, 20.5)': '20≤T<20.5 \u00b0C', '[20.5, 21.0)': '20.5≤T<21 \u00b0C',
        '[21.0, 21.5)': '21≤T<21.5 \u00b0C', '[21.5, 22.0)': '21.5≤T<22 \u00b0C',
        '[22.0, 22.5)': '22≤T<22.5 \u00b0C', '[22.5, 23.0)': '22.5≤T<23 \u00b0C',
        '[23.0, 23.5)': '23≤T<23.5 \u00b0C', '[23.5, 24.0)': '23.5≤T<24 \u00b0C',
        '[24.0, 24.5)': '24≤T<24.5 \u00b0C', '[24.5, 25.0)': '24.5≤T<25 \u00b0C',
        '[25.0, 25.5)': '25≤T<25.5 \u00b0C', '[25.5, 26.0)': '25.5≤T<26 \u00b0C',
        '[26.0, 26.5)': '26≤T<26.5 \u00b0C', '[26.5, 27.0)': '26.5≤T<27 \u00b0C',
        '[27.0, 27.5)': '27≤T<27.5 \u00b0C', '[27.5, 28.0)': '27.5≤T<28 \u00b0C',
        '[28.0, 28.5)': '28≤T<28.5 \u00b0C', '[28.5, 29.0)': '28.5≤T<29 \u00b0C',
        '[29.0, 29.5)': '29≤T<29.5 \u00b0C', '[30.0, 30.5)': '30≤T<30.5 \u00b0C',
        '[30.5, 31.0)': '30.5≤T<31 \u00b0C', '[31.0, 31.5)': '31≤T<31.5 \u00b0C',
        '[31.5, 32.0)': '31.5≤T<32 \u00b0C', '[32.0, 32.5)': '32≤T<32.5 \u00b0C',
        '[32.5, 33.0)': '32.5≤T<33 \u00b0C', '[33.0, 33.5)': '33≤T<33.5 \u00b0C',
        '[33.5, 34.0)': '33.5≤T<34 \u00b0C', '[34.0, 34.5)': '34≤T<34.5 \u00b0C',
        '[34.5, 35.0)': '34.5≤T<35 \u00b0C', '[35.0, 35.5)': '35≤T<35.5 \u00b0C',
        '[35.5, 36.0)': '35.5≤T<36 \u00b0C', '[36.0, 36.5)': '36≤T<36.5 \u00b0C',
    }
    df_mtic = pd.DataFrame(mtic_segment)
    # Modify Y axis
    df_mtic['Inlet Temperature'] = df_mtic['Inlet Temperature'].astype(str)
    df_mtic['Inlet Temperature'] = df_mtic['Inlet Temperature'].map(
        temp_range_dictionary)
    # Export processed data to csv file
    df_mtic.to_csv(
        f'temporary_results/{file[:-4]}_modified.txt', index=True, sep='\t')
    # Graph style
    sns.set(style='whitegrid')
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(14, 8))
    # plot graph
    sns.set_color_codes("muted")
    sns.barplot(x='Number of IT Equipment', y='Inlet Temperature', data=mtic_segment, label=f'{file[:-4]}',
                color='b', ax=ax, order=df_mtic['Inlet Temperature']
                )
    # manipulate x axis to percentage
    ax.set(xlim=(0, 0.4))
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:,.0%}'.format(x) for x in vals])
    # Y axis
    plt.gca().invert_yaxis()
    # Legend
    ax.legend(ncol=2, loc="lower right", frameon=True)
    # Export figure to csv file
    plt.savefig(f'temporary_results/{file[:-4]}_figure', dpi=400)

# combine processed data
filenames2 = glob.glob('temporary_results/*.txt')
list_of_dfs = [pd.read_csv(filename2, delimiter='\t')
               for filename2 in filenames2]
for dataframe2, filename2 in zip(list_of_dfs, filenames2):
    dataframe2['Scenario'] = filename2[18:-13]
combined_df = pd.concat(list_of_dfs, ignore_index=True, axis=0)
combined_df.to_csv('temporary_results/combined_df.txt', index=True)
# Plot Order
y_order2 = temp_range_dictionary.values()
y_order2 = DataFrame(y_order2).copy()
y_order2.columns = ['y_order']
combined_df2 = list(dict.fromkeys(combined_df['Inlet Temperature']))
y_order3 = [x for x in y_order2['y_order'] if x not in combined_df2]
y_order = [x for x in y_order2['y_order'] if x not in y_order3]
# ------------------------------------------------------------plot combined data
plt.figure()
f2, ax2 = plt.subplots(figsize=(14, 8))
sns.barplot(x='Number of IT Equipment', y='Inlet Temperature', data=combined_df, hue='Scenario', palette='tab10',
            order=y_order)
ax2.set(xlim=(0, 0.4))
vals_summary = ax2.get_xticks()
ax2.set_xticklabels(['{:,.0%}'.format(x_summary)
                     for x_summary in vals_summary])
ax2.legend(ncol=2, loc="lower right", frameon=True)
ax2 = plt.gca()
# set the bar border width to 0
plt.setp(ax2.patches, linewidth=0)
# plot background area color
n_shade = 0
while n_shade in range(0, n_temp * 4 + 2):
    ax2.axhspan(n_shade - 0.5, n_shade + 0.5, facecolor='grey', alpha=0.1)
    n_shade += 2
# ax2.set_facecolor('lightblue')
# Y axis
plt.gca().invert_yaxis()
plt.savefig('temporary_results/summary_figure', dpi=400)
