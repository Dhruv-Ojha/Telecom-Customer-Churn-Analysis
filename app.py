import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.title("TELECOM CUSTOMER CHURN ANALYSIS")
st.sidebar.title("TELECOM CUSTOMER CHURN ANALYSIS")

st.sidebar.markdown("This app is a streamlit dashboard to analyze the customer churn data.")

DATA_URL = ("C:\\Users\\Dhruv\\Documents\\ML and Data Analysis Projects\\Telecom Customer Churn Prediction\\preprocessed_data.csv")

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

data = load_data()
if st.sidebar.checkbox("Show raw data", False):
    st.write(data)

st.sidebar.markdown("#### Enter Customer ID")
ci = st.sidebar.text_input('Customer ID')
filtered_data = data[data['customerID'] == ci]
if not filtered_data.empty:
    st.write(filtered_data)
else:
     if ci != "":
         st.write('No data found for the given Customer ID')
 


st.sidebar.markdown("#### Count based on Demographics")
select = st.sidebar.selectbox('Select Demographic Feature', ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Churn'])
select2 = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie Chart'], key=1)

if not st.sidebar.checkbox("Hide", True, key='checkbox1'):
    st.markdown("### Count of customers by demographics")

    label_mapping = {
        'gender': 'Gender',
        'SeniorCitizen': 'Senior Citizen',
        'Partner': 'Partner',
        'Dependents': 'Dependents'
    }


    count = data[select].value_counts().reset_index()
    count.columns = [select, 'Count']
    
    if select2 == "Histogram":
        fig = px.bar(count, x=select, y='Count', color='Count',
                     labels={'Count': 'Count', select: label_mapping[select]},
                     title=f"Number of Customers by {label_mapping[select]}")
        st.plotly_chart(fig)
    else:
        fig1 = px.pie(count, values='Count', names=select,
                      title=f"Number of Customers by {select}")
        st.plotly_chart(fig1)



st.sidebar.markdown("### Number of Customers by Demographics")
select1 = st.sidebar.selectbox('Select Demographic', ['gender', 'SeniorCitizen', 'Partner', 'Dependents'], key=2)
show_count = st.sidebar.checkbox("Show Count", value=False, key=5)

grouped_data = data.groupby([select1, 'Churn']).size().reset_index(name='Count')

if not st.sidebar.checkbox("Hide", True, key='checkbox2'):
    st.markdown(f"### Number of Customers by {select1}")
    fig2 = px.bar(grouped_data, x=select1, y='Count', color='Churn',
                  labels={'Count': 'Count', select1: select1},
                 title=f"Number of Customers by {select1}",
                 height = 600, color_discrete_sequence=['red', 'yellow'])
    st.plotly_chart(fig2)

    if show_count:
        count_data = data.groupby(select1).size().reset_index(name='Total Count')
        count_data['Percentage'] = count_data['Total Count'] / count_data['Total Count'].sum() * 100
        st.write("### Count of Customers by", select1)
        st.table(count_data)





st.sidebar.markdown("### Number of Customers by Service Used")
select2 = st.sidebar.selectbox('Select Service', ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'], key=3)
show_count1 = st.sidebar.checkbox("Show Count", value=False, key=6)

grouped_data1 = data.groupby([select2, 'Churn']).size().reset_index(name='Count')

if not st.sidebar.checkbox("Hide", True, key='checkbox3'):
    st.markdown(f"### Number of Customers by {select2}")
    fig3 = px.bar(grouped_data1, x='Count', y=select2, color='Churn',
                  labels={'Count': 'Count', select2: select2},
                  title=f"Number of Customers by {select2}", barmode = 'stack', orientation='h', height = 400, width = 800,
                  color_discrete_sequence=['gray', 'red'])
    st.plotly_chart(fig3)

    if show_count1:
        count_data = data.groupby(select2).size().reset_index(name='Total Count')
        count_data['Percentage'] = count_data['Total Count'] / count_data['Total Count'].sum() * 100
        st.write(f"### Count of Customers by {select2}")
        st.table(count_data)



st.sidebar.markdown("### Number of Customers by Account Information")
select3 = st.sidebar.selectbox('Select Service', ['Contract', 'PaperlessBilling', 'PaymentMethod'], key=4)
show_count2 = st.sidebar.checkbox("Show Count", value=False, key=9)

grouped_data2 = data.groupby([select3, 'Churn']).size().reset_index(name='Count')

if not st.sidebar.checkbox("Hide", True, key='checkbox4'):
    st.markdown(f"### Number of Customers by {select3}")
    fig4 = px.bar(grouped_data2, y=select3, x='Count', color='Churn',
                  labels={'Count': 'Count', select3: select3},
                  title=f"Number of Customers by {select3}",
                  barmode='stack', orientation='h', height=400, width=800,
                  color_discrete_sequence=['orange', 'blue'],
                  template='plotly_dark')  
    fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)',  
                      paper_bgcolor='rgba(0,0,0,0)',  
                      yaxis={'categoryorder': 'total ascending'})  
    fig4.update_xaxes(showgrid=True, gridcolor='lightgray') 
    fig4.update_yaxes(showgrid=True, gridcolor='lightgray')  
    st.plotly_chart(fig4)

    if show_count2:
        count_data = data.groupby(select3).size().reset_index(name='Total Count')
        count_data['Percentage'] = count_data['Total Count'] / count_data['Total Count'].sum() * 100
        st.write(f"### Count of Customers by {select3}")
        st.table(count_data)


st.sidebar.markdown("### Monthly vs Total Charges Analysis")
show_scatter_plot = st.sidebar.checkbox("Show Scatter Plot", value=True, key='checkbox8')

if show_scatter_plot:
    fig5 = px.scatter(data, x='MonthlyCharges', y='TotalCharges', color='Churn',
                      labels={'MonthlyCharges': 'Monthly Charges', 'TotalCharges': 'TotalCharges'},
                      title='Relationship between Monthly Charges and Total Charges', color_discrete_sequence=['red', 'blue'], height = 500)
    st.plotly_chart(fig5)



st.sidebar.markdown("### Analyzing Monthly and Total Charges with Churn")
plot_type = st.sidebar.selectbox("Select Plot Type", ["Monthly Charges vs Churn", "Total Charges vs Churn"])

if plot_type == "Monthly Charges vs Churn":
    
    monthly_charges_churn = data[data['Churn'] == 'Yes']['MonthlyCharges']
    monthly_charges_no_churn = data[data['Churn'] == 'No']['MonthlyCharges']

    # Plot KDE for Monthly Charges vs Churn
    st.set_option('deprecation.showPyplotGlobalUse', False)  
    sns.kdeplot(monthly_charges_churn, shade=True, label='Churn', alpha=0.5)
    sns.kdeplot(monthly_charges_no_churn, shade=True, label='No Churn', alpha=0.5)
    plt.xlabel('Monthly Charges')
    plt.ylabel('Density')
    plt.title('Monthly Charges vs Churn')
    plt.legend()
    st.pyplot()

elif plot_type == "Total Charges vs Churn":
    
    total_charges_churn = data[data['Churn'] == 'Yes']['TotalCharges']
    total_charges_no_churn = data[data['Churn'] == 'No']['TotalCharges']

    st.set_option('deprecation.showPyplotGlobalUse', False)  
    sns.kdeplot(total_charges_churn, shade=True, label='Churn')
    sns.kdeplot(total_charges_no_churn, shade=True, label='No Churn')
    plt.xlabel('Total Charges')
    plt.ylabel('Density')
    plt.title('Total Charges vs Churn')
    plt.legend()
    st.pyplot()