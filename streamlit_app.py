import streamlit as st
import pandas as pd
import pcr_func as pcr
from pcr_func import ninetysix_plate_planner
from io import BytesIO
import pcr_func as pcr
from PIL import Image

# Title Streamlit app
st.title("SYBR Green qPCR Calculator")
st.markdown(
    "All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used."
)

# Fetch necessary info from user via sidebar (reaction volume, number of primer pairs, number of samples, number of replicates)
st.sidebar.header("PCR Reaction Information")
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
gene_names = []
for primer_index in range(primer_pairs):
    gene_name = st.sidebar.text_input(f"Gene name for Primer Pair {primer_index + 1}")
    gene_names.append(gene_name)

# Get DNA concentration for each sample from user
st.sidebar.header("DNA Concentration Information")
st.sidebar.write("Enter the DNA concentration for each sample in ng/uL:")
dna_concs = []
for sample_index in range(samples):
    conc = st.sidebar.number_input(f"DNA Concentration for Sample {sample_index + 1}")
    dna_concs.append(conc)

# Check if user wants to include controls
st.sidebar.header("Controls")
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
