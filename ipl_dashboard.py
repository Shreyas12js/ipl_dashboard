

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="IPL Batting Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("ipl_batting_summary.csv")
    return df

df = load_data()

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

if year != "All":
    filtered_df = filtered_df[filtered_df["season"] == int(year)]

if player != "All":
    filtered_df = filtered_df[filtered_df["batsman"] == player]

if team != "All":
    filtered_df = filtered_df[filtered_df["batting_team"] == team]

st.write(f"### Showing {len(filtered_df)} records")

# -----------------------------------------
# KPI Metrics
# -----------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Runs", int(filtered_df["total_runs"].sum()))
col2.metric("Average Strike Rate", round(filtered_df["strike_rate"].mean(), 2))
col3.metric("Total Fours", int(filtered_df["fours"].sum()))
col4.metric("Total Sixes", int(filtered_df["sixes"].sum()))

# -----------------------------------------
# -----------------------------------------
# -----------------------------------------
# 1. Top 10 Six Hitters (based on filters)
# -----------------------------------------
st.subheader("💥 Top 10 Six Hitters")

top_sixers = (
    filtered_df.groupby('batsman')['sixes']
    .sum()
    .sort_values(ascending=True)   # ascending order
    .tail(10)                      # last 10 = highest 10
)

fig_six = px.bar(
    x=top_sixers.values,
    y=top_sixers.index,
    orientation="h",
    title="Top 10 Six Hitters (Filtered)",
    labels={"x": "Total Sixes", "y": "Batsman"},
)

st.plotly_chart(fig_six)

#
# -----------------------------------------
# -----------------------------------------
# 2. Season-wise Runs Line Chart
# -----------------------------------------
if player != "All":
    st.subheader(f"📈 Season-wise Runs - {player}")

    player_season = (
        df[df['batsman'] == player]
        .groupby('season')['total_runs']
        .sum()
        .reset_index()
    )

    fig_line = px.line(
        player_season,
        x="season",
        y="total_runs",
        markers=True,
        title=f"Season-wise Runs Trend - {player}"
    )

    st.plotly_chart(fig_line)

#
# Density Plot - Strike Rate
# -----------------------------------------
st.subheader("📈 Density Plot - Strike Rate")
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.kdeplot(filtered_df["strike_rate"], shade=True, ax=ax2)
st.pyplot(fig2)

# -----------------------------------------
# Box Plot - Runs
# -----------------------------------------
st.subheader("📦 Box Plot - Runs")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.boxplot(x=filtered_df["total_runs"], ax=ax3)
st.pyplot(fig3)

# -----------------------------------------
# Violin Plot - Strike Rate
# -----------------------------------------
st.subheader("🎻 Violin Plot - Strike Rate")
fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.violinplot(x=filtered_df["strike_rate"], ax=ax4)
st.pyplot(fig4)
#
# Bell Curve - Runs
# -----------------------------------------
st.subheader("📊 Bell Curve - Total Runs")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.histplot(filtered_df["total_runs"], kde=True, ax=ax1)
st.pyplot(fig1)

# -----------------------------------------
# -----------------------------------------


#
# -----------------------------------------
# Bell Curve - Strike Rate
# -----------------------------------------
st.subheader("📊 Bell Curve - Strike Rate Distribution")

fig_sr, ax_sr = plt.subplots(figsize=(8, 4))
sns.histplot(filtered_df["strike_rate"], kde=True, ax=ax_sr, bins=30)
ax_sr.set_xlabel("Strike Rate")
ax_sr.set_ylabel("Frequency")
st.pyplot(fig_sr)





# -----------------------------------------
# Scatter Plot
# -----------------------------------------
st.subheader("📉 Scatter Plot - Runs vs Balls")
fig5, ax5 = plt.subplots(figsize=(8, 4))
sns.scatterplot(x=filtered_df["balls_faced"], y=filtered_df["total_runs"], ax=ax5)
st.pyplot(fig5)

# -----------------------------------------
# Correlation Heatmap
# -----------------------------------------
st.subheader("🔥 Correlation Heatmap")
num_cols = ["total_runs", "balls_faced", "strike_rate", "fours", "sixes"]
corr = filtered_df[num_cols].corr()

fig6, ax6 = plt.subplots(figsize=(8, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax6)
st.pyplot(fig6)

# -----------------------------------------
# Top Batsmen
# -----------------------------------------
# -----------------------------------------
# P-value for correlation (NO SCIPY)
# -----------------------------------------
import numpy as np
from math import sqrt
from math import erf

st.subheader("📉 Correlation P-value")

# Extract two variables and drop NaNs
x = filtered_df["total_runs"].dropna()
y = filtered_df["balls_faced"].dropna()

# Convert to numpy arrays
x = np.array(x)
y = np.array(y)

# Sample size
n = len(x)

# Pearson correlation
r = np.corrcoef(x, y)[0, 1]

# Calculate t-statistic manually
t_stat = r * sqrt((n - 2) / (1 - r**2))

# Compute p-value (approximation using error function)
# p = 2 * (1 - t_cdf(|t|))  -- but using normal approx
p_value = 2 * (1 - 0.5 * (1 + erf(abs(t_stat) / sqrt(2))))

st.write(f"### 📌 Pearson Correlation: **{r:.3f}**")
st.write(f"### 📌 P-value (approx): **{p_value:.10f}**")

if p_value < 0.05:
    st.success("✔ The correlation is statistically significant (p < 0.05).")
else:
    st.warning("⚠ The correlation is NOT statistically significant.")


# -----------------------------------------
# -----------------------------------------



