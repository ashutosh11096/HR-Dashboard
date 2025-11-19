import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

#Load Hr Dataset

df =pd.read_csv('C:/Users/hites/Desktop/HRDataset_v14.csv')
st.set_page_config(page_title= "HR Dashboard", layout="centered")


#Emp Count
Total_Emp = df['EmpID'].count()
gender_count = df['Sex'].value_counts()
Male_Emp = gender_count.get( 'M ',0)
Female_Emp = gender_count.get('F',0) 
Status = df['EmploymentStatus'].value_counts()
Hire = Status.get('Active',0)
terminated = Status.get('Voluntarily Terminated', Status.get('Terminated for Cause', 0))

#KPI 
left_col, right_col = st.columns([1, 3])  # adjust ratio (2:3)
with left_col:
    with st.container():
        st.metric("Total Employee", Total_Emp)
        st.metric("Male Emp", Male_Emp)
        st.metric("Female Emp", Female_Emp)
        st.metric("Hire", Hire)
        st.metric("Terminations", terminated)

with right_col:
# Donut Chart
    sizes = [Male_Emp, Female_Emp]
    labels = ['Male', 'Female']
    colors = ['#2f4b7c', '#d45087']  # Blue & Pink

    fig1, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        startangle=90,
        wedgeprops={'width': 0.35} ,
        autopct='%1.1f%%',
        pctdistance=1.2,
        labeldistance= 0.4
    )
    ax.axis('equal')
    ax.set_title("Headcount by Gender")



    #Age Range

    df['DOB'] = pd.to_datetime(df['DOB'], errors='coerce', dayfirst=True)
    df.loc[df['DOB'] > pd.Timestamp.today(), 'DOB'] -= pd.DateOffset(years=100)
    today = pd.Timestamp.today()
    df['Age'] = (today - df['DOB']).dt.days // 365
    # Age Range Bins
    bins = [0, 30, 40, 50, 60, 200]
    labels = ['<30', '30-40', '40-50', '50-60', '60+']

    df['Age Range'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    age_range_counts = df['Age Range'].value_counts().sort_index()



    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Headcount by Gender" )
        st.pyplot(fig1)

    with col2:
        st.subheader("Headcount by Age Range" )
        fig2 = st.bar_chart(age_range_counts)
    #Headcount By Department

    Department = df['Department'].value_counts().sort_index()


    fig3, ax = plt.subplots(figsize=(10,6))
    ax.bar(Department.index,Department.values)
    ax.set_title("Employee Distribution by Department")
    ax.set_xlabel("Count")
    plt.tight_layout()


    # Salary Expenses
    Expenses = df.groupby('Department')['Salary'].sum().sort_values()

    fig4, ax = plt.subplots(figsize=(10,6))
    ax.barh(Expenses.index,Expenses.values)
    ax.set_title("Expenses by Department")
    ax.ticklabel_format(style='plain', axis='x')
    for i, v in enumerate(Expenses.values):
        ax.text(v + 10, i, str(int(v)), va='center')

    plt.tight_layout()

    print(df)

    k1,k2 = st.columns(2)

    with k1:
        st.pyplot(fig3)

    with k2:
        st.pyplot(fig4)

st.balloons()
st.snow()


