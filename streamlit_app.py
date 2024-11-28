# Import necessary libraries
import streamlit as st
import pandas as pd
import pcr_func as pcr
from io import BytesIO

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

# Display editable dataframe
st.markdown("Please fill in the DNA concentrations for each gene, then click calculate")
st.data_editor(data)

# Calculate volumes of YSB and DNA for each gene
if st.button("Calculate"):
    for i in range(no_genes):
        data["YSBVol"][i] = pcr.ysb_vol_calc(reaction_vol, no_samples)
        data["DNAVol"][i] = pcr.dna_vol_calc(reaction_vol, no_samples, data["DNAConc"][i])
        buffer = BytesIO()
        data.to_csv(buffer, index=False)
        buffer.seek(0)
        
# Download CSV button
st.download_button(
    label="Download results as CSV",
    data=buffer,
    file_name='qPCR_volumes.csv',
    mime='text/csv'
)

# Download xlsx button
st.download_button(
    label="Download results as Excel",
    data=buffer,
    file_name='qPCR_volumes.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# Download PNG button
st.download_button(
    label="Download results as PNG",
    data=buffer,
    file_name='qPCR_volumes.png',
    mime='image/png'
)

    
    

    







