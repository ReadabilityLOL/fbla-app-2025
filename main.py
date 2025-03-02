import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random
import math
import datetime
from openai import OpenAI

api_key = "7" #replace with api key


def merge_slices(list0, list1):
    from collections import defaultdict
    dict_slices = defaultdict(lambda: 0)
    for val, title in zip(list0, list1):
        dict_slices[title] += val
    return list(dict_slices.values()), list(dict_slices.keys())
thing = dict()

weekly, monthly, yearly = st.tabs(["Weekly", "Monthly","Annually"])

debt = 100000
average_spending = 770
income = 880

random2 = random.randint(5,10)
dates = range(2019, 2019+random2)
for x in range(random2):
    thing[f"{dates[x]}"] = random.randint(10000,1000000)


prices = [100, 200, 33, 90]
organizations = ["Amazon", "Ebay", "Walmart", "Netflix"]
categories = ["Shopping", "Shopping", "Shopping", "Entertainment"]
dates = [datetime.datetime(2024,10,x).date() for x in range(1,5)]


data_df = pd.DataFrame(
    {
        "Organization": organizations,
        "Category": categories,
        "Price": prices,
        "Date":dates,
    }
)


st.markdown(
        """
        <style>
        .stMainBlocContainer {
            max-width:100%;
            width: 95%;
        }

        .st-emotion-cache-mtjnbi {
          width: 100%;
          padding: 6rem 1rem 10rem;
          max-width: 75%;
        }
        </style>
        """,
        unsafe_allow_html=True
)

with weekly.container(border=True):
    col1, col2, col3 = weekly.columns(3, border = True)
    col4, col5 = weekly.columns([3,2], border = True)
    col6, col7 = weekly.columns(2, border = True)

    with col1:
        col1.markdown("###### Total Debt");
        col1.markdown(f"## ${debt}");

    with col2:
        col2.markdown("###### Average Spending");
        col2.markdown(f"## ${average_spending}");

    with col3:
        col3.markdown("###### Income");
        col3.markdown(f"## ${income}");

    with col4:
        col4.subheader("Net Worth over Time")
        col4.line_chart(thing,x_label="Year",y_label="Net Worth")
    
    with col5:

        client = OpenAI(api_key=api_key)
        
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": "You are a helpful AI assistant on our Finance Website"}]
        
        col5.title("Chat with AI-CoPilot")
        
        total_debt = st.session_state.get("total_debt", 0.0)
        monthly_expenses = st.session_state.get("expenses", 0.0)
        
        financial_context = (
            f"Transactions: ${data_df}"
            f"Total debt: ${debt}"
            f"Average Spending: ${average_spending}"
            f"Income: ${income}"
            "Consider this information when providing responses."
        )
        st.session_state["messages"][0]["content"] = financial_context
        
        chat_container = col5
        for message in st.session_state["messages"]:
            if message["role"] != "system":
                with chat_container:
                    col5.chat_message(message["role"]).write(message["content"])
        user_input = col5.text_input("Type your message:", key="user_input4")
        
        if col5.button("Send",key="b2"):
            if user_input:
                st.session_state["messages"].append({"role": "user", "content": user_input})
        
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state["messages"]
                )
        
                ai_message = response.choices[0].message.content
                st.session_state["messages"].append({"role": "assistant", "content": ai_message})
                st.rerun() 

    with col6:
        col6.subheader("Expenses this week")
        r = col6.data_editor(
            data_df,
            hide_index=True,
            num_rows="dynamic",
        )

        prices = r["Price"]
        categories = r["Category"]
    with col7:
        
        labels = categories
        cleanse = lambda x: x if not math.isnan(x)  else 0;

        sizes = [cleanse(x) for x in prices]

        sizes2, labels2 = merge_slices(sizes, labels)

        
        fig1, ax1 = plt.subplots()
        #ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
        ax1.pie(sizes2, labels=labels2, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        col7.pyplot(fig1)

with monthly.container(border=True):
    col1, col2, col3 = monthly.columns(3, border = True)
    col4, col5 = monthly.columns([3,2], border = True)
    col6, col7 = monthly.columns(2, border = True)

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

    with col5:
        client = OpenAI(api_key=api_key)
        
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": "You are a helpful AI assistant."}]
        
        col5.title("Chat with AI-CoPilot")
        
        total_debt = st.session_state.get("total_debt", 0.0)
        monthly_expenses = st.session_state.get("expenses", 0.0)
        
        financial_context = (
            f"Total Debt: ${total_debt}\n"
            f"Monthly Expenses: ${monthly_expenses}\n"
            "Consider this information when providing responses."
        )
        st.session_state["messages"][0]["content"] = financial_context
        
        chat_container = col5
        for message in st.session_state["messages"]:
            if message["role"] != "system":
                with chat_container:
                    col5.chat_message(message["role"]).write(message["content"])
        user_input = col5.text_input("Type your message:", key="user_input2")
        
        if col5.button("Send",key="b1"):
            if user_input:
                st.session_state["messages"].append({"role": "user", "content": user_input})
        
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state["messages"]
                )
        
                ai_message = response.choices[0].message.content
                st.session_state["messages"].append({"role": "assistant", "content": ai_message})
                st.rerun() 
    with col6:
        col6.subheader("Expenses this week")
        r = col6.data_editor(
            data_df,
            hide_index=True,
            num_rows="dynamic",
            key="month-graph"
        )

        prices = r["Price"]
        categories = r["Category"]
    with col7:
        
        labels = categories
        cleanse = lambda x: x if not math.isnan(x)  else 0;

        sizes = [cleanse(x) for x in prices]

        sizes2, labels2 = merge_slices(sizes, labels)

        
        fig1, ax1 = plt.subplots()
        #ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
        ax1.pie(sizes2, labels=labels2, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        col7.pyplot(fig1)


with yearly.container(border=True):
    col1, col2, col3 = yearly.columns(3, border = True)
    col4, col5 = yearly.columns([3,2], border = True)
    col6, col7 = yearly.columns(2, border = True)

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

    with col5:
        client = OpenAI(api_key=api_key)
        
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": "You are a helpful AI assistant."}]
        
        col5.title("Chat with AI-CoPilot")
        
        total_debt = st.session_state.get("total_debt", 0.0)
        monthly_expenses = st.session_state.get("expenses", 0.0)
        
        financial_context = (
            f"Total Debt: ${total_debt}\n"
            f"Monthly Expenses: ${monthly_expenses}\n"
            "Consider this information when providing responses."
        )
        st.session_state["messages"][0]["content"] = financial_context
        
        chat_container = col5
        for message in st.session_state["messages"]:
            if message["role"] != "system":
                with chat_container:
                    col5.chat_message(message["role"]).write(message["content"])
        user_input = col5.text_input("Type your message:", key="user_input")
        
        if col5.button("Send"):
            if user_input:
                st.session_state["messages"].append({"role": "user", "content": user_input})
        
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state["messages"]
                )
        
                ai_message = response.choices[0].message.content
                st.session_state["messages"].append({"role": "assistant", "content": ai_message})
                st.rerun() 


    with col6:
        col6.subheader("Expenses this week")
        r = col6.data_editor(
            data_df,
            hide_index=True,
            num_rows="dynamic",
            key="year-graph"
        )

        prices = r["Price"]
        categories = r["Category"]
    with col7:
        
        labels = categories
        cleanse = lambda x: x if not math.isnan(x)  else 0;

        sizes = [cleanse(x) for x in prices]

        sizes2, labels2 = merge_slices(sizes, labels)

        
        fig1, ax1 = plt.subplots()
        #ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
        ax1.pie(sizes2, labels=labels2, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        col7.pyplot(fig1)



