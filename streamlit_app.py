# Import necessary libraries
import streamlit as st
from io import BytesIO
import pandas as pd
import pcr_func as pcr


# Title Streamlit app
st.title('SYBR Green qPCR Calculator')
st.markdown("All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used.") 
        

# Sidebar with user inputs
st.sidebar.header('User Inputs')
st.sidebar.markdown("Please enter the following information")
reaction_vol = st.sidebar.selectbox('Reaction volume (uL)', [10, 20])
no_genes = st.sidebar.number_input('Number of genes (primer pairs)', min_value=1, step=1)
no_samples = st.sidebar.number_input('Number of samples per gene (primer pair)', min_value=1, step=1)

# Create output dataframe
data = pd.DataFrame(columns = ["Gene", "YSBVol", "DNAVol"])

# Request the names of each gene
if no_genes > 0:
    
    # Dictionary to store gene names
    gene_names = {}
    
    # Loop through the number of genes and request the gene names
    for i in range(1, int(no_genes) + 1):
        gene_name = st.sidebar.text_input(f"Gene {i} name:", key=f"gene_{i}")
        gene_names[f"Gene {i}"] = gene_name

# Add gene names to the dataframe
data["Gene"] = gene_names.values() 

#

# Calculate the volume of yellow sample buffer and DNA for each gene
ysb_dict = {}
dna_dict = {}

for i in range(no_genes):
    ysb_dict[f"Gene {i+1}"] = pcr.ysb_vol_calc(reaction_vol, no_samples)
    dna_dict[f"Gene {i+1}"] = pcr.dna_vol_calc(reaction_vol, no_samples)  









