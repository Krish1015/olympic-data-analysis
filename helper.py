import pandas as pd
import numpy as np
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally

def country_yr_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')

    country = np.unique(df['region'].dropna().values).tolist()

    country.sort()
    country.insert(0,'overall')

    return years, country
df = pd.read_csv('athlete_events.csv')

def fetch_medal_tally(df, year, country):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if country == 'overall' and year == 'overall':
        temp_df = medal_tally
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_tally[medal_tally['region'] == country]
    if year != 'overall' and country == 'overall':
        temp_df = medal_tally[medal_tally['Year'] == year]
    if year != 'overall' and country != 'overall':
        temp_df = medal_tally[(medal_tally['Year'] == year) & (medal_tally['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')


    x["Total"] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Total'] = x['Total'].astype('int')

    return x

