# Import necessary libraries
import streamlit as st
import pandas as pd
import pcr_func as pcr
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image

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
data = pd.DataFrame(columns = ["Gene", "YSBVol", "DNAVol", "DNAConc"]) 

# Display editable dataframe
st.markdown("Please fill in the Name of each gene DNA concentrations for each sample, then click calculate")
st.dataframe(data)

# Calculate volumes of YSB and DNA for each gene
if st.button("Calculate"):
    csv_buffer = BytesIO()
    for i in range(no_genes):
        data.at[i, "YSBVol"] = pcr.ysb_vol_calc(reaction_vol, no_samples)
        data.at[i, "DNAVol"] = pcr.dna_vol_calc(reaction_vol, no_samples, data["DNAConc"][i])
data.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)
        
# Download CSV button
st.download_button(
    label="Download results as CSV",
    data=csv_buffer,
    file_name='qPCR_volumes.csv',
    mime='text/csv'
)

# Download xlsx button
st.download_button(
    label="Download results as Excel",
    data= csv_buffer,
    file_name='qPCR_volumes.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# Image download button 
if st.button("Download results as image"):
    fig, ax = plt.subplots(figsize=(len(data.columns)*2, len(data) * 0.6 )) # Adjust figure size based on dataframe size
    ax.axis("tight")
    ax.axis("off")
    
    # Create table plot
    table = ax.table(
        cellText=data.values,
        colLabels=data.columns,
        cellLoc='center',
        loc='center',
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(len(data.columns))))
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    img_buffer.seek(0) 
    
# Reset button
if st.button("Reset"):
    st.caching.clear_cache()
    st.experimental_rerun()
    


    
    

    







