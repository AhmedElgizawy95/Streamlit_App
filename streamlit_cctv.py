#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np 
import streamlit as st

import altair as alt
from PIL import Image


# In[2]:
# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def set_background(png_file):
#     bin_str = get_base64(png_file)
#     page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# set_background('download2.png')
#page_bg_img = '''
#<style>
#.stApp{
#background-image: url("download2.jpg");
#background-size: cover;
#}
#</style>
#'''

#st.markdown(page_bg_img, unsafe_allow_html=True)
image = Image.open('download.jpg')
st.image(image, use_column_width=200)



# In[3]:


st.title('Attendance Report')


# In[4]:
# In[22]:


uploaded_file = st.file_uploader("Upload xlsx", type=".xlsx")

# use_example_file = st.checkbox(
#     "Use example file", False, help="Use in-built example file to demo the app"
# )

ab_default = None
result_default = None


# if use_example_file:
#     uploaded_file = "2022-10-13_10-44-20_644.xlsx"
#     ab_default = ["Personnel Name"]
#     result_default = ["Detection Time Face "]
    
    
###############################################   
    
    
Names = []
StartDate = []
EndDate = []  

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    

    df['InvoiceDate'] = pd.to_datetime(df['Detection Time'],format = '%Y-%m-%d %H:%M:%S')
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['Day'] = df['InvoiceDate'].dt.day
    df['Hour'] = df['InvoiceDate'].dt.hour
    df['Mins'] = df['InvoiceDate'].dt.minute
    df['WeekDay'] = df['InvoiceDate'].dt.day_name()
    df['WeekDayCase'] = df['WeekDay'].apply(lambda x : 'WeekEnd' if str(x).lower() in ['saturday','sunday'] else 'WeekDay')
    dfs = df[['Personnel Name','InvoiceDate','Year', 'Month', 'Day', 'Hour', 'Mins',
           'WeekDay', 'WeekDayCase']]
    dfs.dropna(subset=['Personnel Name'],inplace = True)
    first_day = dfs["Day"].min()
    last_day = dfs["Day"].max()
    for name in dfs['Personnel Name'].unique():
        for day in range(first_day,last_day + 1 ,1):
            print("Name" + " " + dfs[dfs["Personnel Name"] == name]['Personnel Name'].unique()[0])
            Names.append(dfs[dfs["Personnel Name"] == name]['Personnel Name'].unique()[0])
            print("Start" + " " +str(dfs[(dfs["Personnel Name"] == name) & (dfs["Day"] == day)]['InvoiceDate'].min()))
            StartDate.append(str(dfs[(dfs["Personnel Name"] == name) & (dfs["Day"] == day)]['InvoiceDate'].min()))
            print("End" + " " +str(dfs[(dfs["Personnel Name"] == name) & (dfs["Day"] == day)]['InvoiceDate'].max()))
            EndDate.append(str(dfs[(dfs["Personnel Name"] == name) & (dfs["Day"] == day)]['InvoiceDate'].max()))
            print("-----------------------------------------")
dataN = {'Names':Names,'Start Date':StartDate,'End Date':EndDate}
data = pd.DataFrame(dataN)

    

st.markdown("### Data preview")
st.dataframe(data.head())

st.markdown("### Select columns for analysis")
with st.form(key="my_form"):
    ab = st.multiselect(
        "A/B column",
        options = data['Names'].unique() ,
        
        help ="Select which column refers to your A/B testing labels.",
        default=ab_default,
        )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.dataframe(data[data["Names"] ==ab[0]])
#st.dataframe(data[data["Names"] == ab])
 #In[24]:
csv = data.to_csv(index=False,encoding="utf-8-sig")
st.download_button(label='Download',data=csv,file_name='AR.csv',mime='text/csv')

#st.download_button('Download',)
# dataM = data.to_excel('states.xlsx', sheet_name = "states", index = False)

# st.download_button('Download', 'states.xlsx')


# In[20]:





# In[ ]:





# In[ ]:




