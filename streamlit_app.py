# Import necessary libraries
import streamlit as st
from io import BytesIO
import pandas as pd

# Title Streamlit app
st.title('SYBR Green qPCR Calculator. All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used.')

# Sidebar with user inputs
st.sidebar.header('User Inputs')
reaction_vol = st.sidebar.selectbox('Reaction volume (uL)', [10, 20])
no_genes = st.sidebar.number_input('Number of genes')
no_samples = st.sidebar.number_input('Number of samples per gene')






