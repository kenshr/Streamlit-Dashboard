import pandas as pd
import streamlit as st
import altair as alt
from numerize.numerize import numerize
import re

st.set_page_config(
  page_title='ChAD',
  layout='wide',
  initial_sidebar_state='expanded'
)

@st.cache_data
def get_data():
  df = pd.read_csv('../data/chat_dataset.csv')
  df['date'] = pd.to_datetime(df['timestamp'])
  return df

df = get_data()

header_left, header_mid, header_right = st.columns([1,3,1],gap='large')

with header_mid:
  st.title('Chat Analytics Dashboard')

with st.sidebar:
  user_filter = st.multiselect(
    label='Select User',
    options=sorted(df['user'].unique(), key=lambda x: int(re.search(r'\d+', x).group())),
    default='user_1'
  )
  all_users = st.checkbox(
    label="Select all users",
    key="allUsers"
  )
  if all_users:
    user_filter = sorted(df['user'].unique(), key=lambda x: int(re.search(r'\d+', x).group()))

  channel_filter = st.multiselect(
    label='Select Channel',
    options=sorted(df['channel'].unique(), key=lambda x: int(re.search(r'\d+', x).group())),
    default=df['channel'][0]
  )
  all_channels = st.checkbox(
    label="Select all channels",
    key="allChannels"
  )
  if all_channels:
    channel_filter = sorted(df['channel'].unique(), key=lambda x: int(re.search(r'\d+', x).group()))

# Downselected data
filtered_df = df.query('user == @user_filter & channel == @channel_filter')
donation_month_agg_df = (
  filtered_df.groupby(filtered_df.date.dt.month)['donation'].sum()
  .rename(index={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'})
  .reset_index()
  .rename(columns={'date':'Month','donation':'Donation ($)'})
)

# Top-level metrics
total_active_users = len(filtered_df['user'].unique())
total_interactions = len(filtered_df)
total_donations = float(filtered_df['donation'].sum())

metric1,metric2,metric3=st.columns(3,gap='large')

with metric1:
  st.image('imgs/user.png',use_column_width='Auto')
  st.metric(label='Total Active Users',value=numerize(total_active_users))

with metric2:
  st.image('imgs/interaction.png',use_column_width='Auto')
  st.metric(label='Total Interactions',value=numerize(total_interactions))

with metric3:
  st.image('imgs/donation.png',use_column_width='Auto')
  st.metric(label='Total Donations',value='$' + str(numerize(total_donations)))

# MoM Donation Graph
chart_title_left, chart_title_mid, chart_title_right = st.columns([1,3,1],gap='large')

with chart_title_mid:
  st.subheader("Month over Month Donations")

mom_chart = (
  alt.Chart(
    data=donation_month_agg_df,
  )
  .mark_bar()
  .encode(
  x="Month",
  y="Donation ($)",
  )
)
st.altair_chart(mom_chart,use_container_width=True)
