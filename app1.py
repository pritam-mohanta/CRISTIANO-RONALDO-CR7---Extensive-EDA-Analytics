import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import io

plt.style.use("ggplot")

st.set_page_config(page_title="CRISTIANO RONALDO (CR7) - Extensive EDA & Analytics", layout="wide")

st.sidebar.title("📊 UR-Cristiano (CR7) Analytics")

st.sidebar.image("cr7.png", use_column_width=True)

#The operations we can do take it as list 

sections = ["Introduction", 
"Basic Exploration", 
"Goals per Competition", 
"Goals per Season", 
"Goals per Club", 
"Goals per Playing Position", 
"Goals per Game Minute", 
"Goals per Type", 
#"Scoreline After Goals",
#"Opponents", 
"Favorite Opponents", 
"Assists", 
"Goals per Venue"]

# Create a Radio Buttion for taking Input 

selections = st.sidebar.radio("Navigate to", sections)

df=pd.read_csv('data.csv')

if selections == "Introduction":
    st.title("⚽ CR7 - Extensive EDA & Analytics")
    st.subheader("Cristiano Roanaldo - All Club Goals Statistics")

    st.write("""
    **Cristiano Ronaldo dos Santos Aveiro** is a Portuguese professional footballer who plays as a forward for Al-Nassr and captains the Portugal national team.
    
    - **Current team**: Al-Nassr (#7 / Forward)
    - **Born**: February 5, 1985 (age 39 years), Funchal, Portugal
    - **Height**: 1.87 m
    - **Partner**: Georgina Rodríguez (2017–)
    - **Salary**: 2OO million EURO (2024)
    - **Children**: Cristiano Ronaldo Jr., Alana Martina, Eva Maria, Mateo Ronaldo
    """)

elif selections == "Basic Exploration":
    st.subheader("🔍 Basic Exploration")
    st.write("### Data Snapshot")
    st.dataframe(df.head())
    st.write("### Data Info")
    # df.info() -> gave us pandas core class and also buffer string so we have to convert to get the value so we use io (input output)
    buffer = io.StringIO()
    df.info(buf = buffer)
    s = buffer.getvalue()
    st.text(s)

    st.write("### Unique Values in Each Column")
    st.dataframe(pd.DataFrame(df.apply(lambda col:len(col.unique())), columns = ["Unique Values Count"]))
    st.write("### Summary Statistics for Categorical Columns")
    st.dataframe(df.describe(include=['object']))

    # st.dataframe(df.describe(include=['object']).T)

elif selections == "Goals per Competition":
    st.subheader("🏆 Goals per Competition")
    # for chart we use ploty ###########
    fig = px.histogram(df, x = 'Competition', color='Club', title = "Goals per Competition", 
                 height=500,hover_name = "Club", hover_data=['Competition', 'Club'])
    st.plotly_chart(fig)
    st.write("### Competition Goal Counts")
    st.dataframe(df.Competition.value_counts())

elif selections == "Goals per Season":
    st.subheader("📅 Goals per Season")
    fig = px.histogram(df, x = 'Season', color='Club', title = "Goals per Season", 
                 height=500,hover_name = "Club", hover_data=['Season', 'Club'])
    st.plotly_chart(fig)
    st.write("### Season Goal Counts")
    st.dataframe(df.Season.value_counts())

elif selections == "Goals per Club":
    st.subheader("🏅 Goals per Club")
    fig1 = px.histogram(df, x = 'Club', color='Season', title = "Goals per Club - Season", 
                 height=500,hover_name = "Season", hover_data=['Competition', 'Season', 'Club'])
    fig2 = px.histogram(df, x = 'Club', color='Competition', title = "Goals per Club - Competition", 
                 height=500,hover_name = "Competition", hover_data=['Competition', 'Season', 'Club'])
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

elif selections == "Goals per Playing Position":
    st.subheader("⚽ Goals per Playing Position")
    fig = px.histogram(df, x = 'Playing_Position', color='Club', title = "Goals per Playing Position", 
                 height=500,hover_name = "Club", hover_data=['Playing_Position','Competition', 'Season', 'Club'])
    st.plotly_chart(fig)

# first we get all minutes -> give it in bins and then cut the minutes based on bins
elif selections == "Goals per Game Minute":
    st.subheader("⏰ Goals per Game Minute")
    df['Minute'] = df['Minute'].str.extract('(\d+)', expand=False).fillna(0).astype(int) #get the minutes
    bins = [0,15,30,45,60,75,90,105,120]
    labels = ['0-15', '15-30', '30-45', '45-60','60-75', '75-90', '90-105','105-120']
    df['Minute_Bin'] = pd.cut(df['Minute'], bins = bins, labels=labels, right=False) #cut the minutes based on bins
    fig = px.histogram(df, x = 'Minute_Bin', title = "Goals per Game Minute", color = 'Club', height=500)
    st.plotly_chart(fig)

elif selections == "Goals per Type":
    st.subheader("🏹 Goals per Type")
    fig = px.histogram(df, x = 'Type', title = "Goals per Typee", color = 'Club', height=500)
    st.plotly_chart(fig)

#elif selections == "Scoreline After Goals":
    #st.subheader("🔢 Scoreline After Goals")
    #top_20_scores = df['At_score'].value_counts().nlargest(20).index
    #df_top_20 = df[df['At_score'].isin(top_20_scores)]

    #fig, ax = plt.subplots(figsize=(15,7))
    #sns.countplot(x='At_score', data=df_top_20, order = top_20_scores, ax = ax)
    ##ax.set_title("Top 20 Scoresheets after Scoring", fontsize = 20)
    #st.pyplot(fig)

elif selections == "Favorite Opponents":
    st.subheader("❤️ Top 20 Opponents")
    top_20_opponent = df['Opponent'].value_counts().nlargest(20).index
    df_top_20 = df[df['Opponent'].isin(top_20_opponent)]
    fig, ax = plt.subplots(figsize=(30,10))
    sns.countplot(x='Opponent', data = df_top_20, order = top_20_opponent, ax=ax)
    ax.set_title("Goal per Opponents", fontsize = 20)
    plt.xticks(rotation=45)
    st.pyplot(fig) 

#elif selections == "Favorite Opponents":
    #st.subheader("❤️ Favorite Opponents", )
    #fig, ax = plt.subplots(figsize=(15,7))
    #fav_opponents_df = df['Opponent'].value_counts()[df['Opponent'].value_counts()>15]
    #sns.countplot(x='Opponent', data = df[df['Opponent'].isin(fav_opponents_df.index)], order = fav_opponents_df.index, ax=ax)
    #ax.set_title("Favorite Opponents", fontsize = 20)
    #st.pyplot(fig)

elif selections == "Assists":
    st.subheader("🤝 Assists")

    top_10_assist = df['Goal_assist'].value_counts().nlargest(10).index

    df_top_10 = df[df['Goal_assist'].isin(top_10_assist)]

    fig, ax = plt.subplots(figsize=(15,7))

    sns.countplot(x = 'Goal_assist', data = df_top_10, order = top_10_assist, ax = ax)

    ax.set_title("Top 10 Assists", fontsize = 20)

    st.pyplot(fig)

elif selections == "Goals per Venue":
    st.subheader("🏟️ Goals per Venue")
    fig, ax = plt.subplots(figsize = (15,7))
    sns.countplot(x = 'Venue', data = df, order = df['Venue'].value_counts().index, ax = ax)
    ax.set_title("Home & Away", fontsize = 20)
    st.pyplot(fig)  
