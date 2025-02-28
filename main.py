import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random

thing = dict()

weekly, monthly, annually = st.tabs(["Weekly", "Monthly","Annually"])


random2 = random.randint(5,10)
dates = range(2019, 2019+random2)
for x in range(random2):
    thing[f"{dates[x]}"] = random.randint(10000,1000000)


prices = [100, 200, 33, 90]
organizations = ["Amazon", "Ebay", "Walmart", "Netflix"]
categories = ["Shopping", "Shopping", "Shopping", "Entertainment"]

data_df = pd.DataFrame(
    {
        "Organization": organizations,
        "Category": categories,
        "Price": prices,
    }
)


with weekly.container(border=True):
    col1, col2, col3 = weekly.columns(3, border = True)
    col4, col5 = weekly.columns([3,2], border = True)
    col6, col7 = weekly.columns(2, border = True)

    with col1:
        col1.markdown("###### Total Debt");
        col1.markdown("## $999999");
        col1.markdown("*0.5% interest per month*");

    with col2:
        col2.markdown("###### Average Spending");
        col2.markdown("## $77");
        col2.markdown("*+3% from last month*");

    with col3:
        col3.markdown("###### Income");
        col3.markdown("## $888");
        col3.markdown("*+6% from last month*");

    with col4:
        col4.subheader("Net Worth over Time")
        col4.line_chart(thing,x_label="Year",y_label="Net Worth")

    with col6:
        col6.subheader("Expenses this week")
        col6.data_editor(
            data_df,
            hide_index=True,
        )
    with col7:
        labels = categories
        sizes = prices
        explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        col7.pyplot(fig1)

