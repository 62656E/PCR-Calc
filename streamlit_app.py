import streamlit as st
import pandas as pd
import pcr_func as pcr
from pcr_func import ninetysix_plate_planner
from io import BytesIO
import pcr_func as pcr
from PIL import Image
import base64

# Title Streamlit app
st.title("SYBR Green qPCR Calculator")
st.markdown(
    "All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used."
)

# Fetch necessary info from user via sidebar (reaction volume, number of primer pairs, number of samples, number of replicates)
with st.expander("PCR Reaction Information", expanded=True): 
    st.sidebar.write("Enter the following information:")
    st.sidebar.write("1. Total volume of the PCR reaction in uL")
    reaction_volumes = [10, 20]
    reaction_vol = st.sidebar.selectbox("Reaction Volume", reaction_volumes)
    st.sidebar.write("2. Number of primer pairs")
    primer_pairs = st.sidebar.number_input("Number of Primer Pairs", min_value=1, value=1)
    st.sidebar.write("3. Number of samples")
    samples = st.sidebar.number_input("Number of Samples", min_value=1, step=1)
    st.sidebar.write("4. Number of replicates")
    reps = st.sidebar.number_input("Number of Replicates", min_value=1, step=1)

# Get gene names for each primer pair
with st.expander("Gene/Primer Pair Information", expanded=True):
    st.sidebar.write("Enter the gene name for each primer pair:")
    gene_names = []
    for primer_index in range(primer_pairs):
        gene_name = st.sidebar.text_input(f"Gene name for Primer Pair {primer_index + 1}")
        gene_names.append(gene_name)

# Get DNA concentration for each sample from user
with st.expander("DNA Concentration Information", expanded=True):
    st.sidebar.write("Enter the DNA concentration for each sample in ng/uL:")
    dna_concs = []
    for sample_index in range(samples):
        conc = st.sidebar.number_input(f"DNA Concentration for Sample {sample_index + 1}")
        dna_concs.append(conc)

# Check if user wants to include controls
with st.expander("Control Information", expanded=True):
    controls = st.sidebar.checkbox("Include Controls")

# Calculate plate layout based on user input
if st.sidebar.button("Calculate Plate Layout"):
    plate_layout, vol_plate_layout = ninetysix_plate_planner(
        samples, 
        dna_concs, 
        reaction_vol, 
        gene_names, 
        reps, 
        controls
    )
    
    # Display plate_layout and vol_plate_layout in a table
    st.header("Volume Plate Layout:")
    st.markdown("Format of below cells is gene/primer pair name-sample number-repeat.")
    # Display the volume layout for each well in the 96-well plate
    st.dataframe(plate_layout)
    st.header("Volume Plate Layout:")
    st.dataframe(vol_plate_layout)
    
# Save the plate layout and volume layout as CSV files
if st.button("Save Plate Layout"):
    csv = plate_layout.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="plate_layout.csv">Download Plate Layout as CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

if st.button("Save Volume Plate Layout"):
    csv = vol_plate_layout.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="vol_plate_layout.csv">Download Volume Plate Layout as CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

# Add reset button
if st.sidebar.button("Reset"):
    st.caching.clear_cache()
    st.experimental_rerun()
