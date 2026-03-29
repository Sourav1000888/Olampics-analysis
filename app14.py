import streamlit as st
import preprocess, medal_tally
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Olampics Analysis

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocess.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select as option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis')
)
# st.dataframe(df)

if user_menu == "Medal Tally":
    st.sidebar.header('Medal Tally')
    years, country = medal_tally.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select year', years)
    selected_country = st.sidebar.selectbox('Select country', country)

    medal_tally = medal_tally.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal tally in '+ str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' overall performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country +  ' performace in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.title('Top Statistics')
    edition = df['Year'].nunique()
    city = df['City'].nunique()
    sport = df['Sport'].nunique()
    event = df['Event'].nunique()
    name = df['Name'].nunique()
    region = df['region'].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Edition')
        st.subheader(edition)
    with col2:
        st.subheader('Hosts')
        st.subheader(city)
    with col3:
        st.subheader('Sport')
        st.subheader(sport)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Event')
        st.subheader(event)
    with col2:
        st.subheader('Nation')
        st.subheader(region)
    with col3:
        st.subheader('Athletes')
        st.subheader(name)

    nation_over_year = medal_tally.participate_nation(df, 'region')
    st.title('Nations over the years')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot('Year', 'region', data=nation_over_year)
    st.pyplot(fig)


    event_over_year = medal_tally.participate_nation(df, 'Event')
    st.title('Events over the years')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot('Year', 'Event', data=event_over_year)
    st.pyplot(fig)


    athlete_over_year = medal_tally.participate_nation(df, 'Name')
    st.title('Athlete over the years')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot('Year', 'Name', data=athlete_over_year)
    st.pyplot(fig)


    st.title('No. of events over year (every sport)')
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event',
                               aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)


    st.title('Most successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport ', sport_list)

    res = medal_tally.most_sucessfull(df, selected_sport)
    st.table(res.reset_index(drop=True)) 


if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country ', country_list)
    country_df = medal_tally.year_wise_medal_tally(df, selected_country)
    st.title(selected_country + ' Medal Tally over the years')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot('Year', 'Medal', data=country_df)
    st.pyplot(fig)


    st.title(selected_country + ' in the sports')
    pt = medal_tally.country_event_heatmap(df, selected_country)
    if pt.empty:
        st.warning('No Information')
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)


    st.title('Top atheletes of ' + selected_country)
    top_10_df = medal_tally.most_sucessfull_country_wise(df, selected_country)
    st.table(top_10_df.reset_index(drop=True))