import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------------------------
# Load Data
# -----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("./ipl_batting_summary.csv")
    return df

df = load_data()

st.set_page_config(page_title="IPL Batting Dashboard", layout="wide")

st.title("🏏 IPL Batting Performance Dashboard")

# -----------------------------------------
# Sidebar Filters
# -----------------------------------------
st.sidebar.header("Filters")

years = sorted(df["season"].unique())
players = sorted(df["batsman"].unique())
teams = sorted(df["batting_team"].unique())

year = st.sidebar.selectbox("Select Year", ["All"] + list(years))
player = st.sidebar.selectbox("Select Player", ["All"] + list(players))
team = st.sidebar.selectbox("Select Team", ["All"] + list(teams))

# -----------------------------------------
# Apply Filters
# -----------------------------------------
filtered_df = df.copy()


