# Import necessary libraries
import streamlit as st
from io import BytesIO
import pandas as pd

# Title Streamlit app
st.title('SYBR Green qPCR Calculator. All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used.')

# Sidebar with user inputs
st.sidebar.header('User Inputs')
reaction_vol = st.sidebar.selectbox('Reaction volume (uL)', [10, 20])
no_genes = st.sidebar.number_input('Number of genes (primer pairs)')
no_samples = st.sidebar.number_input('Number of samples per gene (primer pair)')

# Create output dataframe
data = pd.DataFrame(columns = ["Gene", "YSBVol", "DNAVol"])

# Request the names of each gene
if no_genes > 0:
    
    # Dictionary to store gene names
    gene_names = {}
    
    for i in range(1, no_genes + 1):
        gene_name = st.text_input(f"Gene {i} name:", key=f"gene_{i}")
        gene_names[f"Gene {i}"] = gene_name









