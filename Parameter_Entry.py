import streamlit as st
import pcr_func as pcr
import pickle as pkl 
import pandas as pd

# Title page
st.title("SYBR Green qPCR calculator")

# Fetch necessary info from user via sidebar (reaction volume, number of primer pairs, number of samples, number of replicates)
with st.expander("PCR Reaction Information", expanded=True):
    st.write("Enter the following information:")
    st.write("1. Total volume of the PCR reaction in uL")
    reaction_volumes = [10, 20]
    reaction_vol = st.selectbox("Reaction Volume", reaction_volumes)
    st.write("2. Number of primer pairs")
    primer_pairs = st.number_input(
        "Number of Primer Pairs", min_value=1, value=1
    )
    st.write("3. Number of samples")
    samples = st.number_input("Number of Samples", min_value=1, step=1)
    st.write("4. Number of replicates")
    reps = st.number_input("Number of Replicates", min_value=1, step=1)

# Get gene names for each primer pair
with st.expander("Gene/Primer Pair Information", expanded=True):
    st.write("Enter the gene name for each primer pair:")
    gene_names = []
    for primer_index in range(primer_pairs):
        gene_name = st.text_input(
            f"Gene name for Primer Pair {primer_index + 1}"
        )
        gene_names.append(gene_name)

# Get DNA concentration for each sample from user
with st.expander("DNA Concentration Information", expanded=True):
    st.write("Enter the DNA concentration for each sample in ng/uL:")
    dna_concs = []
    for sample_index in range(samples):
        conc = st.number_input(
            f"DNA Concentration for Sample {sample_index + 1}"
        )
        dna_concs.append(conc)

# Check if user wants to include controls
with st.expander("Control Information", expanded=True):
    inc_controls = st.checkbox("Include Controls")
