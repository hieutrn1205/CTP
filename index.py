from calendar import month
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config( # head tag

    page_title="NYC Inspection", 
    page_icon="random",
    layout="wide",
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'https://github.com/hieutrn1205/CTP',
        'Report a bug': "https://github.com/hieutrn1205/CTP/issues/new",
        'About': """
                ***Streamlit app*** that visualizes New York City Inspection data 
                """ #supports markdown
    })

df = pd.read_csv("./data/data.csv")
df.columns = df.columns.str.lower()
df["inspection date"] = pd.to_datetime(df["inspection date"])
error = df["longitude"] <-77
df = df[~error]
df = df.dropna(subset=['longitude', 'latitude',"borough"])
df["borough"] = np.where(df["borough"]=="QUEENS", "Queens", df["borough"])
df["borough"] = np.where(df["borough"]=="MANHATTAN", "Manhattan", df["borough"])
df["borough"] = np.where(df["borough"]=="BRONX", "Bronx", df["borough"])
df["borough"] = np.where(df["borough"]=="BROOKLYN", "Brooklyn", df["borough"])
df["year"] = df["inspection date"].dt.year
df["year"]=df["year"]


def create_map(df,borough,year,ind):
    cond1 = df["year"] > 1900
    cond2 = df["year"] > 1900
    cond3 = df["year"] > 1900
    if borough != "All":
        cond1 = df["borough"] == borough
    if year != "All":
        cond2 = df["year"] == int(year)
    if ind != "All":
        cond3 = df["industry"] == ind
    df = df[cond1 & cond2 & cond3]
    st.map(df)

def pie_chart(df, borough, year, industry):
    cond1 = df["year"] > 1900
    cond2 = df["year"] > 1900
    cond3 = df["year"] > 1900
    if borough != "All":
        cond1 = df["borough"] == borough
    if industry != "All":
        cond2 = df["industry"] == industry
    if year != "All":
        cond3 = df["year"] == int(year)
    df = df[cond1 & cond2 & cond3]
    labels = [index for index in df["inspection result"].value_counts().index]
    value = [value for value in df["inspection result"].value_counts().values]
    fig = go.Figure(data=[go.Pie(labels = labels, values= value)])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig

def stacked_bar(df, borough, year, industry):
    cond1 = df["year"] > 1900
    cond2 = df["year"] > 1900
    cond3 = df['year'] > 1900
    if borough != "All":
        cond1 = df["borough"] == borough
    if year != "All":
        cond2 = df["year"] == int(year)
    if industry != "All":
        cond3 = df["industry"] == industry
    temp_df1 = df[cond1 & cond2 & cond3]
    key = ["No Violation Issued", "Violation Issued"]
    months = sorted([month for month in df["inspection date"].dt.month.unique()])
    no_violated= list()
    violated = list()
    key = ["No Violation Issued", "Violation Issued"]
    for month in months:
        temp_cond = temp_df1["inspection date"].dt.month == month
        value  = dict(temp_df1[temp_cond]["inspection result"].value_counts())
        for k in value:
            if k == key[0]:
                no_violated.append(value[k])
            if k == key[1]:
                violated.append(value[k])
    temp_df = pd.DataFrame(columns = key)
    temp_df["No Violation Issued"] = no_violated
    temp_df["Violation Issued"] = violated
    temp_df["Month"] = months
    
    fig = px.bar(temp_df, x="Month", y=["No Violation Issued", "Violation Issued"],width=1920*0.7, height=1080*0.7)
    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 1,
            dtick = 1
        )
    )

    fig

#Creating values options for user interface

#Creating borough options
borough_values = list(np.insert(df['borough'].unique(),0,values="All"))
borough_values.remove(borough_values[-1])

#Creating industry options


with st.sidebar: #creates side bar
    borough = st.selectbox(
        label="Select Borough",
        options = borough_values
    )
    if borough != "All":
        year_values =list(np.insert(sorted([str(i) for i in df["year"].unique()]),0,values="All"))
        year = st.selectbox(
            label="Select Inspection Year",
            options = year_values
        )
    else:
        year_values =list(np.insert(sorted([str(i) for i in df["year"].unique()]),0,values="All"))
        year = st.selectbox(
            label="Select Inspection Year",
            options = year_values
        )
    if borough != "All":
        industry_values = list(np.insert(df[df["borough"] == borough]["industry"].value_counts().index, 0, values = "All"))
        industry = st.selectbox(
            label = "Industry Selection",
            options = industry_values
        )
    else:
        industry_values = list(np.insert(df["industry"].value_counts().index, 0, values = "All"))
        industry = st.selectbox(
            label = "Industry Selection",
            options = industry_values
        )

def create_metric(df, borough, year, industry):
    original = len(df)
    cond1 = df["year"] > 1900
    cond2 = df["year"] > 1900
    cond3 = df["year"] > 1900
    if borough != "All":
        cond1 = df["borough"] == borough
    if industry != "All":
        cond2 = df["industry"] == industry
    if year != "All":
        cond3 = df["year"] == int(year)
    df = df[cond1 & cond2 & cond3]
    num_inspection = len(df)
    temp = round((num_inspection/original)*100)
    temp = str(temp) + "%"
    st.write(industry, ' industry in ', borough, ' borough  is ', temp, 'of all inspections in ', year)

#Split to cols
st.title("NYC Inspection Data Visualizer") # H1 tag
create_map(df, borough, year, industry)
create_metric(df, borough, year, industry)
st.title("Inspection results for " + industry + " industry in " + borough + " borough in " + year)
pie_chart(df, borough, year, industry)
st.title("Number of Violation and Non-Violation in " + borough + " for industry " + industry + " in " + year)
stacked_bar(df, borough, year, industry)



