import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import streamlit as st


import helper
import prepeossesor

df = pd.read_csv('athlete_events.csv')
region_df  = pd.read_csv('noc_regions.csv')

df = prepeossesor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally','Overall analysis','Country-wise Analysis','Athelete wise Analysis')
)
df = df.loc[~df.index.duplicated(),:].copy()
#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_yr_list(df) # import country and years list from the helper file

    # creating dropdown menu for year and country
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Counter", country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title("Overall Medal Tally")
    if selected_year != 'overall' and selected_country == "overall":
        st.title("Medal Tally for the year "+ str(selected_year))
    if selected_year != 'overall' and selected_country != "overall":
        st.title("Medal Tally of "+ str(selected_country) + ' in '+ str(selected_year))
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country + "overall performance ")

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    st.table(medal_tally)


if user_menu == 'Overall analysis': # For selecting the Overall Analysis option
    edition = df['Year'].unique().shape[0]-1 #Total no. of editins
    sports = df['Sport'].unique().shape[0] # Total no. of unique sports
    events = df['Event'].unique().shape[0] # No. of events played throughout all olympics
    host_city = df['City'].unique().shape[0] # No. of Host cities of olympic
    Total_country_perticipated = df['region'].unique().shape[0] # Total No. of countries participated in olympic
    atheletes = df['Name'].unique().shape[0] # Total no. of olympics participate till now

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3) # Creation three coloumns in a row for showing the informations

    with col1: # Edition
        st.header('Editions')
        st.title(edition)
    with col2: # Host cities
        st.header('Hosts')
        st.title(host_city)
    with col3: # #Sport
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3) # Second Row

    with col1: # Events
        st.header('Events')
        st.title(events)
    with col2: # nations
        st.header('Nations')
        st.title(Total_country_perticipated)
    with col3: # atheletes
        st.header('Atheletes')
        st.title(atheletes)

    #Ploting of the datas
    st.title('No. of countries over time')
    nations_over_time = helper.data_over_time(df,'region') # No. of nations over time
    fig = px.line(nations_over_time,x = 'Edition',y = 'No. of region')
    st.plotly_chart(fig)

    st.title('No. of events over time')
    events_over_time = helper.data_over_time(df, 'Event')  # No. of nations over time
    fig = px.line(events_over_time, x='Edition', y='No. of Event')
    st.plotly_chart(fig)

    st.title('No. of atheletes over time')
    atheletes_over_time = helper.data_over_time(df, 'Name')  # No. of nations over time
    fig = px.line(atheletes_over_time, x='Edition', y='No. of Name')
    st.plotly_chart(fig)

    ##  Plotting a heat map for using pivot table as How many events were there for each sport over the time
    st.title('No. of events in each sports over the years' )
    fig,ax = plt.subplots(figsize = (22,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    x_heat = x.pivot_table(index = 'Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(x_heat, annot= True)
    st.pyplot(fig)

    ## Printing most successfull atheletes
    st.title("Most successful Atheletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')
    selected_sport = st.selectbox('Select a sport', sport_list)
    most_successful_atheles = helper.most_successful(df,selected_sport)
    st.table(most_successful_atheles)

if user_menu == 'Country-wise Analysis':
    country_list = np.unique(df['region'].dropna().values).tolist() #Creating the country_list
    country_list.sort()
    st.sidebar.header("Country-wise Analysis") # title
    selected_country = st.sidebar.selectbox('Select one country', country_list) #creating dropdown menu for country
    country_df  =  helper.country_wise_medal_tally(df,selected_country) #import the country_wise medal data list from helper files

    # Print
    fig = px.line(country_df, x = 'Year', y = 'Medal')
    st.title('Year wise total medal received by ' + selected_country)
    st.plotly_chart(fig)


    st.title('Successful sports for countries over the time')

    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize = (22,20))
    ax = sns.heatmap(pt, annot= True)
    st.pyplot(fig)

    st.title("Top 15 atheletes of "+ selected_country)
    top15_df = helper.most_successful_atheletes_contry_wise(df, selected_country)
    st.table(top15_df)

if user_menu == 'Athelete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df["Medal"] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df["Medal"] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df["Medal"] == 'Bronze']['Age'].dropna()

    fig = ff._distplot.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                       show_hist =False, show_rug=False)
    st.plotly_chart(fig)