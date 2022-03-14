# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:21:46 2022

@author: farhanfarooq
"""

import pandas as pd
#import numpy as np

#from sklearn.ensemble import RandomForestClassifier
from pickle import load

import streamlit as st

html_temp = """
    <div style="background-color:wine;padding:10px">
    <h2 style="color:white;text-align:center">Incident Impact Predictor </h2>
    </div>
    """
st.markdown(html_temp, unsafe_allow_html=True)
st.sidebar.header('Input parameters')

def user_input_features():
    
    number = st.sidebar.text_input("number")
    priority = st.sidebar.selectbox("priority", ('', '1 - Critical', '2 - High', '3 - Moderate', '4 - Low'))
    urgency = st.sidebar.selectbox("urgency", ('', '1 - High','2 - Medium', '3 - Low'))
    caller_id= st.text_input("caller_id")
    sys_mod_count= st.text_input("sys_mod_count")
    sys_updated_by= st.text_input("sys_updated_by")
    assigned_to= st.text_input("assigned_to=")
    resolved_by= st.text_input("resolved_by")
    sys_created_by= st.text_input("created_by")
    opened_by=st.text_input("opened_by")
    
    data = {'urgency':urgency,
            'priority':priority,
            'number':number,
            'opened_by':opened_by,
            'caller_id':caller_id,
            'sys_mod_count':sys_mod_count,
            'sys_updated_by':sys_updated_by,
            'assigned_to':assigned_to,
            'resolved_by':resolved_by,
            'sys_created_by':sys_created_by}
    
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

st.subheader('Input parameters')
st.write(input_df)

# load the model
rf_model = load(open('RandomForest.pkl', 'rb'))

# Define the impact scale
impact_scale = {1:'High',
                2:'Medium',
                3:'Low'}

# Default values to fill if input box is empty
default_vals = {'urgency':'2 - Medium',
                'priority':'3 - Moderate',
                'number':'INC0019396',
                'opened_by':'Opened by  17'}

if st.button("Predict"):
    for col in input_df.columns:
        #input_df[col] = input_df[col].apply(lambda x: x.strip(' -HighMediumLowCriticalINCOpenedby')).astype('int')
        input_df[col] = input_df[col].apply(lambda x: x.strip(' -HighMediumLowCriticalINCOpenedby') if x!='' else default_vals[col].strip(' -HighMediumLowCriticalINCOpenedby')).astype('int')
    
    #st.write(input_df)
    result = rf_model.predict(input_df)
    st.subheader('Prediction')
    st.success('{} impact'.format(impact_scale[result[0]]))
