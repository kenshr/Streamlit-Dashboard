import pandas as pd
import streamlit as st
import plotly.express as px
# from numerize.numerize import numerize

st.set_page_config(
  page_title='Dashboard Template',
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
  st.title('Chat Dashboard Template')

with st.sidebar:
  user_filter = st.multiselect(
    label='Select User',
    options=df['user'],
    default=df['user'][0]
  )

  time_filter = st.multiselect(
    label='Select Time Range',
    options=df['date'],
    default=df['date'][0]
  )


