import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import altair as alt

# Configuration de la page
st.set_page_config(page_title="Dashboard Streaming", layout="wide")

# Connexion à SQLite
engine = create_engine("sqlite:///data/streaming.db")

# Lecture des données
df = pd.read_sql("SELECT * FROM events", engine)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

st.title("🎬 Dashboard de la plateforme de streaming")
st.markdown("Analyse de l'activité des utilisateurs et des types d'événements")

# Filtres
with st.sidebar:
    st.header("🧭 Filtres")
    date_range = st.date_input("📆 Plage de dates", [df["date"].min(), df["date"].max()])
    if len(date_range) == 2:
        df = df[(df["date"] >= date_range[0]) & (df["date"] <= date_range[1])]

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🎥 Total événements", len(df))
with col2:
    st.metric("👤 Utilisateurs uniques", df["username"].nunique())
with col3:
    top_event = df["event_type"].value_counts().idxmax()
    st.metric("📊 Événement le + courant", top_event)

st.markdown("---")

# Graphiques en colonnes
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Événements par type")
    event_counts = df["event_type"].value_counts().reset_index()
    event_counts.columns = ["event_type", "count"]
    chart_event = alt.Chart(event_counts).mark_bar().encode(
        x=alt.X("event_type", sort="-y"),
        y="count",
        color="event_type"
    ).properties(height=300)
    st.altair_chart(chart_event, use_container_width=True)

with col2:
    st.subheader("👥 Activité des utilisateurs")
    user_counts = df["username"].value_counts().nlargest(10).reset_index()
    user_counts.columns = ["username", "count"]
    chart_users = alt.Chart(user_counts).mark_bar().encode(
        x=alt.X("username", sort="-y"),
        y="count",
        color=alt.value("#FF4B4B")
    ).properties(height=300)
    st.altair_chart(chart_users, use_container_width=True)

# Évolution temporelle
st.subheader("📈 Évolution des événements dans le temps")
daily_events = df.groupby("date").size().reset_index(name="event_count")
chart_time = alt.Chart(daily_events).mark_line(point=True).encode(
    x="date:T",
    y="event_count:Q",
    tooltip=["date:T", "event_count"]
).properties(height=400)
st.altair_chart(chart_time, use_container_width=True)

st.markdown("___")
st.caption("🗂️ Données extraites depuis une base locale SQLite — Réalisé avec Streamlit, Pandas, SQLAlchemy et Altair.")
